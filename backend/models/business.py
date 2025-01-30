from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.userbase import UserBase


class Business(UserBase):
    """
    Represents a business entity in the system.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        business_name (str): The name of the business. Cannot be null.
        phone (str): The phone number of the business. Cannot be null.
        reservations (relationship): A relationship to the Reservation model, indicating that one business can have many reservations.
    """


    __tablename__ = "business"
    business_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    # Link to Reservation (1 Business -> Many Reservations)
    reservations = relationship("Reservation", back_populates="business")
