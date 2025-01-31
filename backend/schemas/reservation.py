from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class ReservationBase(BaseModel):
    """
    ReservationBase schema for reservation data.

    Attributes:
        business_id (UUID): Unique identifier for the business.
        fair_id (UUID): Unique identifier for the fair.
        place_id (UUID): Unique identifier for the place.
        reserved_date (datetime): Date and time when the reservation is made.
        payment_id (UUID): Unique identifier for the payment.
    """

    business_id: UUID
    fair_id: UUID
    place_id: UUID
    reserved_date: datetime
    payment_id: UUID


class ReservationCreate(ReservationBase):
    """
    A class used to represent the creation of a Reservation.

    This class inherits from ReservationBase and does not add any additional
    attributes or methods. It is used to distinguish between creating a new
    reservation and other operations that might be performed on a reservation.
    """

    pass


class ReservationResponse(ReservationBase):
    """
    ReservationResponse schema for reservation responses.

    Attributes:
        id (UUID): Unique identifier for the reservation.

    Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs.
    """

    id: UUID

    class Config:
        orm_mode = True
