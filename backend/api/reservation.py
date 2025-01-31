import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.db.session import get_db

from backend.crud.reservation import reservation_crud
from backend.crud.fair import fair_crud
from backend.crud.place import place_crud
from backend.crud.business import business_crud
from backend.schemas.reservation import ReservationCreate, ReservationResponse


router = APIRouter()


@router.post(
    "/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    business_email: str, fair_name: str, place_cordinates: str , db: AsyncSession = Depends(get_db)
) -> ReservationResponse:
    """
    Create a new reservation for a place.
    """
    buisness = await business_crud.get_by_email(db=db, email=business_email)
    if not buisness:
        logger.error(f"Error creating reservation: Business {business_email} not found.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business not found.",
        )
    fair = await fair_crud.get_by_name(db=db, name=fair_name)
    if not fair:
        logger.error(f"Error creating reservation: Fair {fair_name} not found.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fair not found.",
        )
    place = await place_crud.get_place_by_cordinates(db, place_cordinates)
    if not place:
        logger.error(f"Error creating reservation: Place {place_cordinates} not found.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Place not found.",
        )
    payment = None
    reservation = ReservationCreate(
        business_id=buisness.id,
        fair_id=fair.id,
        payment_id=payment,
        place_id=place.id,
    )
    try:
        reservation = await reservation_crud.create_reservation(db=db,business=buisness, place=place, fair=fair, reservation_in=reservation)
        logger.info(f"Reservation created successfully: {reservation}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )

    return reservation


@router.delete("/reservation/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(reservation_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Delete a reservation by reservation ID.
    """
    try:
        reservation = await reservation_crud.delete_reservation(db=db, reservation_id=reservation_id)
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return

@router.delete("/reservation/expired_payment_delete_reservatoin/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def expired_payment_delete_reservatoin(reservation_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Delete a reservation with expired payment.
    """
    try:
        reservation = await reservation_crud.expired_payment_delete_reservatoin(db=db, reservation_id=reservation_id)
        if reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reservation not deleted.",
            )
        logger.info(f"Reservation deleted successfully: {reservation}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong1.",
        )
    return
