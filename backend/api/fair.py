from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from loguru import logger

from backend.db.session import get_db

from backend.crud.fair import fair_crud

from backend.schemas.fair import FairCreate, FairResponse


router = APIRouter()


@router.post("/crete_fair", response_model=FairResponse, status_code=status.HTTP_201_CREATED)
async def create_fair(
    fair_in: FairCreate, db: AsyncSession = Depends(get_db)
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
        logger.error(
            f"Error creating fair: Name {fair_in.name} already registered."
        )
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

@router.post("/change_fair", response_model=FairResponse, status_code=status.HTTP_200_OK)
async def change_fair(fair_in: FairCreate, db: AsyncSession = Depends(get_db)):
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