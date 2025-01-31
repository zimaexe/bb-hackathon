import jwt
from datetime import timedelta, datetime, timezone
from backend.core.config import settings
from backend.schemas.token import Token
from backend.db.session import get_db, AsyncSession
from backend.crud.bussiness import
async def create_access_token(data: dict) -> Token:
    """
    Generates a new access token with an expiration time.

    Args:
        data (dict): The data to be encoded into the token.

    Returns:
        Token: An object containing the encoded JWT access token and its expiration time.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=settings.secret_key, algorithm=settings.algorithm)
    return Token(access_token=encoded_jwt, expiration_date=expire)

async def decode_access_token(token: Token):
    try:
        data = jwt.decode(jwt=token.access_token, key=settings.secret_key, algorithms=settings.algorithm)
    except Exception as e:
        pass
    return data

async def auth_user(db: AsyncSession, email: str,  password: str):
    bussiness = get_by_email
