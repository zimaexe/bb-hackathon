from sqlalchemy import String, INT, BOOLEAN
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseModel, fair_place_association


class Place(BaseModel):
    """
    Represents a Place entity in the database.
    Attributes:
        __tablename__ (str): The name of the database table.
        place_name (str): The name of the place, unique and nullable.
        place_zona (int): The zone of the place, nullable.
        place_cordinates (str): The coordinates of the place, unique and nullable.
        place_reservated (bool): Indicates if the place is reserved, defaults to False.
        fairs (List[Fair]): Many-to-Many relationship with the Fair entity.
        reservations (List[Reservation]): One-to-Many relationship with the Reservation entity, limited to one per Fair via constraint.
    """


    __tablename__ = "place"

    place_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    place_zona: Mapped[int] = mapped_column(INT, nullable=True)
    place_cordinates: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=True
    )
    place_reservated: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    # Many-to-Many with Fair
    fairs = relationship(
        "Fair", secondary=fair_place_association, back_populates="places"
    )
    # 1 Place -> Many Reservations (but limited to 1 per Fair via constraint)
    reservations = relationship("Reservation", back_populates="place")
