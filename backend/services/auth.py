import jwt
from loguru import logger
from datetime import timedelta, datetime, timezone
from backend.core.config import settings
from backend.schemas.token import Token, TokenData
from backend.db.session import get_db, AsyncSession
from backend.crud.business import business_crud
from backend.models.business import Business
from backend.crud.admin import admin_crud
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from pydantic import ValidationError
from fastapi import status

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={"admin": "admin"},
)


async def create_access_token(data: dict) -> Token:
    """
    Generates a new access token with an expiration time.

    Args:
        data (dict): The data to be encoded into the token.

    Returns:
        Token: An object containing the encoded JWT access token and its expiration time.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode, key=settings.secret_key, algorithm=settings.algorithm
    )
    return Token(access_token=encoded_jwt, expiration_date=expire, token_type="bearer")


async def decode_access_token(token: Token):
    """
    Decodes the given access token using JWT.

    Args:
        token (Token): The token object containing the access token to be decoded.

    Returns:
        dict: The decoded data from the access token if decoding is successful.

    Raises:
        Exception: If an error occurs during decoding, it logs the error and raises the exception.
    """

    try:
        data = jwt.decode(
            jwt=token.access_token,
            key=settings.secret_key,
            algorithms=settings.algorithm,
        )
        return data
    except Exception as e:
        logger.error(f"While decoding jwt token exception occurred: {e}")


async def auth_business(db: AsyncSession, email: str, password: str):
    """
    Authenticate a business user by email and password.
    Args:
        db (AsyncSession): The database session.
        email (str): The email address of the business user.
        password (str): The plain text password of the business user.
    Returns:
        Business or None: The authenticated business user object if authentication is successful, otherwise None.
    """

    business = await business_crud.get_by_email(db=db, email=email)

    if not business:
        return

    if not Business.verify_password(
        plain_password=password, hashed_password=business.password
    ):
        return

    return business


async def auth_admin(db: AsyncSession, email: str, password: str):
    """
    Authenticate an admin user by email and password.
    Args:
        db (AsyncSession): The database session.
        email (str): The email of the admin user.
        password (str): The password of the admin user.
    Returns:
        The authenticated admin user if the credentials are valid, otherwise None.
    """

    admin = await admin_crud.get_by_email(db=db, email=email)

    if not admin:
        return

    if not Business.verify_password(
        plain_password=password, hashed_password=admin.password
    ):
        return

    return admin


async def get_current_user_email(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
):
    """
    Asynchronously retrieves the current user's email based on the provided security scopes and token.
    Args:
        security_scopes (SecurityScopes): The security scopes required for the request.
        token (str): The JWT token provided for authentication.
        db (AsyncSession): The database session dependency.
    Returns:
        str: The email of the authenticated user.
    Raises:
        HTTPException: If the credentials are invalid or the user does not have the required permissions.
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, email=email)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    user = await admin_crud.get_by_email(db=db, email=token_data.email)
    if user:
        return user.email

    user = await business_crud.get_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user.email
