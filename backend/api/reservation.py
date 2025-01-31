import uuid

from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from typing import Annotated

from backend.db.session import get_db
from backend.crud.reservation import reservation_crud
from backend.crud.fair import fair_crud
from backend.crud.place import place_crud
from backend.crud.business import business_crud
from backend.schemas.reservation import ReservationCreate, ReservationResponse
from backend.services.auth import get_current_user_email

router = APIRouter()


@router.post(
    "/create_reservation", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
        fair_name: str, place_cordinates: str, business_email: Annotated[
        str, Security(get_current_user_email)
    ], db: AsyncSession = Depends(get_db),
) -> ReservationResponse:
    """
    Create a new reservation for a place.
    """

    if await reservation_crud.is_place_reserved(db=db, place_cordinates=place_cordinates, fair_name=fair_name):
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail="Place already was registred")

    reservation = await reservation_crud.create_reservation(db=db, business=business_email, place=place_cordinates, fair=fair_name)

    if not reservation:
        logger.error(f"Exception occurred while making reservation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )

    return reservation


@router.delete("/delete_reservation_by_id", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation_id(reservation_id: uuid.UUID, business_email: Annotated[
        str, Security(get_current_user_email)
    ], db: AsyncSession = Depends(get_db)):
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

@router.delete("/delete_unpaid_reservations", status_code=status.HTTP_204_NO_CONTENT)
async def expired_payment_delete_reservatoin(db: AsyncSession = Depends(get_db)):
    """
    Delete a reservation with expired payment.
    """
    await reservation_crud.expired_payment_delete_reservatoin(db=db)

@router.delete("/delete_reservation", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(business_email: Annotated[
        str, Security(get_current_user_email)
    ], db: AsyncSession = Depends(get_db)):
    try:
        b = await business_crud.get_by_email(db=db, email=business_email)
        await delete_reservation_id(reservation_id=b.reservations[-1].id, business_email=business_email, db=db)
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return
