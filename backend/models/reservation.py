from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PUUID
from sqlalchemy.orm import mapped_column, relationship
from backend.models.base import BaseModel


class Reservation(BaseModel):
    """
    Reservation model representing a reservation entity in the system.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        business_id (UUID): Foreign key referencing the business entity.
        payment_id (UUID): Foreign key referencing the payment entity, must be unique.
        fair_id (UUID): Foreign key referencing the fair entity.
        place_id (UUID): Foreign key referencing the place entity.
    Constraints:
        __table_args__ (tuple): Unique constraint ensuring one place per fair per reservation.
    Relationships:
        business (relationship): Relationship to the Business model.
        payment (relationship): Relationship to the Payment model.
        fair (relationship): Relationship to the Fair model.
        place (relationship): Relationship to the Place model.
    """

    __tablename__ = "reservation"

    business_id = mapped_column(PUUID, ForeignKey("business.id"))
    payment_id = mapped_column(PUUID, ForeignKey("payment.id"), unique=True)
    fair_id = mapped_column(PUUID, ForeignKey("fair.id"))
    place_id = mapped_column(PUUID, ForeignKey("place.id"))

    # Unique Constraint: 1 Place per Fair per Reservation
    __table_args__ = (
        UniqueConstraint("fair_id", "place_id", name="uq_reservation_fair_place"),
    )

    # Relationships
    business = relationship("Business", back_populates="reservations")
    payment = relationship("Payment", back_populates="reservation")
    fair = relationship("Fair", back_populates="reservations")
    place = relationship("Place", back_populates="reservations")
