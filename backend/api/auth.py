# register for fair
# pay for fair
# cancel reservation

# pay

# get buisness active reservation

from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from backend.db.session import get_db

from backend.crud.business import business_crud
from backend.crud.admin import admin_crud
from backend.schemas.token import Token
from backend.schemas.admin import AdminCreate, AdminResponse, AdminUpdate
from backend.schemas.business import BusinessCreate, BusinessResponse
from backend.services.auth import (
    auth_business,
    create_access_token,
    auth_admin,
    get_current_user_email,
)

router = APIRouter()


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> Token:
    """
    Handles the login process for obtaining an access token.
    This function authenticates the user based on the provided credentials and
    returns an access token with appropriate scopes.
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (AsyncSession): The database session dependency.
    Returns:
        Token: The generated access token.
    Raises:
        HTTPException: If the authentication fails for both admin and business users.
    """
    admin = await auth_admin(
        db=db, email=form_data.username, password=form_data.password
    )
    if admin:
        return await create_access_token(
            data={"sub": form_data.username, "scopes": "admin"}
        )

    business = await auth_business(
        db=db, email=form_data.username, password=form_data.password
    )
    if not business:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await create_access_token({"sub": form_data.username, "scopes": ""})


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=BusinessResponse
)
async def register_business(
    business_in: BusinessCreate, db: AsyncSession = Depends(get_db)
) -> BusinessResponse:
    """
    Registers a new business.
    Args:
        business_in (BusinessCreate): The business data to create.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(get_db).
    Returns:
        BusinessResponse: The created business response.
    Raises:
        HTTPException: If the email is already used (status code 226).
        HTTPException: If an internal server error occurs (status code 500).
    """
    business = await business_crud.get_by_email(db=db, email=business_in.email)
    if business:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED, detail="email already used"
        )

    try:
        business = await business_crud.create_business(db=db, business_in=business_in)
        logger.info(f"Business created successfully: {business}")
        status.HTTP_201_CREATED
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return business


@router.post(
    "/add_admin", response_model=AdminResponse, status_code=status.HTTP_201_CREATED
)
async def add_admin(
    admin_in: AdminCreate,
    get_current_user_email: Annotated[
        str, Security(get_current_user_email, scopes=["admin"])
    ],
    db: AsyncSession = Depends(get_db),
) -> AdminResponse:
    """
    Add a new admin user.
    Args:
        admin_in (AdminCreate): The data required to create a new admin.
        get_current_user_email (Annotated[str, Security]): The email of the current user, obtained through security scopes.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(get_db).
    Returns:
        AdminResponse: The response containing the created admin's details.
    Raises:
        HTTPException: If the email is already used (status code 226).
        HTTPException: If an internal server error occurs (status code 500).
    """

    admin = await admin_crud.get_by_email(db=db, email=admin_in.email)
    if admin:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED, detail="email already used"
        )

    try:
        admin = await admin_crud.create_admin(db=db, admin_in=admin_in)
        logger.info(f"Admin created successfully: {admin}")
        status.HTTP_201_CREATED
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return admin

@router.post("/change_admin", response_model=AdminResponse, status_code=status.HTTP_200_OK)
async def change_admin(admin_in: AdminUpdate, user_email: Annotated[
        str, Security(get_current_user_email, scopes=["admin"])
    ], db: AsyncSession = Depends(get_db)):
    try:
        await admin_crud.change_admin(db=db, admin_in=admin_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/change_business", status_code=status.HTTP_200_OK, response_model=BusinessResponse)
async def change_business(business_in: BusinessCreate,business_email: Annotated[
        str, Security(get_current_user_email)
    ], db: AsyncSession = Depends(get_db)):
    try:
        await business_crud.change_business(db=db, email=business_email, admin_in=business_in)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)