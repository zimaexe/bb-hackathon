from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.crud.base import BaseCRUD
from backend.models.reservation import Reservation
from backend.schemas.reservation import ReservationCreate, ReservationUpdate


class ReservationCRUD(BaseCRUD[Reservation, ReservationCreate, ReservationUpdate]):
    """
    ReservationCRUD class for CRUD operations on the Reservation model.
    """
