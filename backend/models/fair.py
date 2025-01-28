from typing import Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID
from backend.models.base import BaseModel


class Fair(BaseModel):
    """
    Represents a Fair model.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        name (str): The name of the fair.
        start_day (datetime): The starting date of the fair.
        end_day (datetime): The ending date of the fair.
        fair_places (Optional[list[UUID]]): A list of UUIDs representing the places associated with the fair.
    """

    __tablename__ = "fair"
    name: Mapped[str]
    start_day: Mapped[datetime]
    end_day: Mapped[datetime]
    fair_places: Mapped[Optional[list[UUID]]] = mapped_column(JSONB, default=list)
