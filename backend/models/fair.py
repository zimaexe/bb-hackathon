from sqlalchemy.orm import Mapped, relationship
from datetime import datetime
from backend.models.base import BaseModel, fair_place_association


class Fair(BaseModel):
    """
    Represents a Fair entity.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (Mapped[str]): The name of the fair.
        start_day (Mapped[datetime]): The start date of the fair.
        end_day (Mapped[datetime]): The end date of the fair.
        places (relationship): A many-to-many relationship with the Place entity.
        reservations (relationship): A one-to-many relationship with the Reservation entity.
    """

    __tablename__ = "fair"
    name: Mapped[str]
    start_day: Mapped[datetime]
    end_day: Mapped[datetime]

    # Many-to-Many with Place
    places = relationship(
        "Place", secondary=fair_place_association, back_populates="fairs", lazy="selectin"
    )
    # 1 Fair -> Many Reservations
    reservations = relationship("Reservation", back_populates="fair", lazy="selectin")
