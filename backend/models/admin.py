from passlib.context import CryptContext

from backend.models.userbase import UserBase

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class Admin(UserBase):
    """
    Admin model that inherits from UserBase.

    Attributes:
        __tablename__ (str): The name of the table in the database.

    """

    __tablename__ = "admin"
