from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from backend.models.base import BaseModel


class Paymnet(BaseModel):
    """
    Represents a payment record in the database.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        payment_status (str): The status of the payment, default is "pending".
        reservation_id (UUID): The unique identifier for the associated reservation.
    """

    __tablename__ = "paymnet"
    payment_status: Mapped[str] = mapped_column(default="pendign")
    reservation_id: Mapped[UUID]
