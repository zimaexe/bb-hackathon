from typing import Optional
from uuid import UUID
from sqlalchemy import String, INT, BOOLEAN
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import BaseModel


class Place(BaseModel):
    """
    Place model representing a location with various attributes.
    Attributes:
        place_name (str): The name of the place, unique and up to 50 characters.
        place_zona (int): The zone identifier of the place.
        place_cordinates (str): The coordinates of the place, unique and up to 50 characters.
        place_reservated (bool): Indicates if the place is reserved, defaults to False.
        fairs (Optional[list[UUID]]): A list of UUIDs representing fairs associated with the place, stored as JSONB.
    """

    __tablename__ = "place"

    place_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    place_zona: Mapped[int] = mapped_column(INT, nullable=True)
    place_cordinates: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=True
    )
    place_reservated: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    fairs: Mapped[Optional[list[UUID]]] = mapped_column(JSONB, default=list)
