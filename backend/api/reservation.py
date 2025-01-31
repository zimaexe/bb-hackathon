from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.db.session import get_db

from backend.crud.reservation import reservation_crud
from backend.schemas.reservation import ReservationCreate, ReservationResponse


router = APIRouter()


@router.post(
    "/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    reservation_in: ReservationCreate, db: AsyncSession = Depends(get_db)
) -> ReservationResponse:
    """
    Create a new reservation.
    """
    logger.info(
        f"Creating reservation for place {reservation_in.place_id} at fair {reservation_in.fair_id}"
    )
    reservation = await reservation_crud.create_reservation(
        db=db, reservation_in=reservation_in
    )
    logger.info(f"Reservation created successfully: {reservation}")
    return reservation
