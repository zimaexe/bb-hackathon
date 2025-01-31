from sqlalchemy import String
from passlib.context import CryptContext
from sqlalchemy.orm import Mapped, mapped_column
from hashlib import sha256

from backend.core.config import settings
from backend.models.base import BaseModel


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserBase(BaseModel):
    """
    UserBase is an abstract base model for user-related data.

    Attributes:
        email (Mapped[str]): The email address of the user, which is a required field.
        password (Mapped[str]): The password of the user, which is a required field.

    Methods:
        hash_password(password: str) -> str:
            Args:
                password (str): The plaintext password.
            Returns:
                str: The hashed password.

        verify_password(plain_password: str, hashed_password: str) -> bool:
            Args:
                plain_password (str): The plaintext password.
                hashed_password (str): The hashed password.
            Returns:
                bool: True if the password matches, False otherwise.
    """

    __abstract__ = True

    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password with a secret key and Argon2.
        :param password: The plaintext password.
        :return: The hashed password.
        """
        salted_password = sha256((password + settings.secret_key).encode()).hexdigest()
        return pwd_context.hash(salted_password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plaintext password against a hashed password.
        :param plain_password: The plaintext password.
        :param hashed_password: The hashed password.
        :return: True if the password matches, False otherwise.
        """
        salted_password = sha256(
            (plain_password + settings.secret_key).encode()
        ).hexdigest()
        return pwd_context.verify(salted_password, hashed_password)
