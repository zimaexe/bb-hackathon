from uuid import UUID
from sqlalchemy.orm import Mapped
from backend.models.base import BaseModel


class Reservation(BaseModel):
    """
    Represents a reservation in the system.
    Attributes:
        business_id (UUID): The unique identifier for the business associated with the reservation.
        fair_id (UUID): The unique identifier for the fair associated with the reservation.
        place_id (UUID): The unique identifier for the place associated with the reservation.
        payment_id (UUID): The unique identifier for the payment associated with the reservation.
    """

    __tablename__ = "reservation"
    business_id: Mapped[UUID]
    fair_id: Mapped[UUID]
    place_id: Mapped[UUID]
    payment_id: Mapped[UUID]
