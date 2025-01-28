from typing import Optional

from sqlalchemy import String
from passlib.context import CryptContext
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from backend.models.userbase import UserBase

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class Business(UserBase):
    """
    Represents a business entity.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        business_name (str): The name of the business. Cannot be null.
        phone (str): The phone number of the business. Cannot be null.
        reservations (Optional[UUID]): The reservations associated with the business.
    """

    __tablename__ = "business"
    business_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    reservations: Mapped[Optional[UUID]]
