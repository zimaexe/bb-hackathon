from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from typing import Annotated
from backend.db.session import get_db
from backend.services.auth import get_current_user_email
from backend.crud.fair import fair_crud
from backend.crud.business import business_crud
from backend.schemas.fair import FairCreate, FairResponse
from backend.schemas.business import BusinessResponse
from backend.crud.payment import payment_crud
from backend.schemas.payment import PaymentResponse
from backend.schemas.place import PlaceResponse
router = APIRouter()


@router.post(
    "/create_fair", response_model=FairResponse, status_code=status.HTTP_201_CREATED
)
async def create_fair(
    fair_in: FairCreate, user_email: Annotated[
        str, Security(get_current_user_email, scopes=["admin"])
    ], db: AsyncSession = Depends(get_db)
) -> FairResponse:
    """
    Create a new fair.
    This function creates a new fair entry in the database. It first checks if a fair with the given name already exists.
    If it does, it raises an HTTP 400 error. If not, it attempts to create the fair and returns the created fair's details.
    If any exception occurs during the creation process, it raises an HTTP 500 error.
    Args:
        fair_in (FairCreate): The fair data to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).
    Returns:
        FairResponse: The created fair's details.
    Raises:
        HTTPException: If the fair name is already registered (HTTP 400) or if an error occurs during creation (HTTP 500).
    """

    logger.info(f"Creating fair with name: {fair_in.name}")
    db_fair = await fair_crud.get_by_name(db=db, name=fair_in.name)
    if db_fair:
        logger.error(f"Error creating fair: Name {fair_in.name} already registered.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name already registered.",
        )

    try:
        fair = await fair_crud.create_fair(db=db, fair_in=fair_in)
        logger.info(f"Fair created successfully: {fair}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return fair


@router.post(
    "/change_fair", response_model=FairResponse, status_code=status.HTTP_200_OK
)
async def change_fair(fair_in: FairCreate, user_email: Annotated[
        str, Security(get_current_user_email, scopes=["admin"])
    ], db: AsyncSession = Depends(get_db)):
    """
    Change the details of an existing fair.
    Args:
        fair_in (FairCreate): The new details of the fair to be updated.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(get_db).
    Returns:
        Fair: The updated fair information.
    Raises:
        HTTPException: If an error occurs during the update process, an HTTP 500 error is raised with a generic error message.
    Logs:
        Logs the success message with the updated fair information if the update is successful.
        Logs the error message if an exception occurs during the update process.
    """

    try:
        fair = await fair_crud.change_fair(db=db, fair_in=fair_in)
        logger.info(f"Fair info cahnged successufully: {fair}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return fair


@router.get("/get_all_active_fairs", response_model=list[FairResponse], status_code=status.HTTP_200_OK)
async def get_all_fairs(db: AsyncSession = Depends(get_db)) -> list[FairResponse]:
    """
    Retrieve all fairs.
    Args:
        db (AsyncSession): The database session.
    Returns:
        List[FairResponse]: A list of all fairs in the database.
    """

    fairs = await fair_crud.get_all_active_fairs(db=db)
    return [FairResponse.model_validate(fair) for fair in fairs]

@router.get("/info", response_model=list[BusinessResponse])
async def get_all_info(db: AsyncSession = Depends(get_db)):
    fairs = await fair_crud.get_all_active_fairs(db=db)
    if not fairs:
        raise HTTPException(status_code=404, detail="active fair was not found")

    all_business = []
    for fair in list(fairs):
        for reservation in list(fair.reservations):
            all_business.append(( await business_crud.get_by_id(db=db, obj_id=reservation.business_id)))

    return all_business

@router.get("/all_payments", response_model=list[PaymentResponse])
async def get_payments(user_email: Annotated[
        str, Security(get_current_user_email)
    ], db: AsyncSession = Depends(get_db)):
    b = await business_crud.get_by_email(db=db, email=user_email)
    paymnet = []
    for reservation in b.reservations:
        paymnet.append(await payment_crud.get_by_id(db=db, obj_id=reservation.payment_id))

    return paymnet

@router.post('/get_fair_places')
async def get_places(fair_name: str, db: AsyncSession = Depends(get_db)):
    return await fair_crud.get_places(db=db, fair_name=fair_name)