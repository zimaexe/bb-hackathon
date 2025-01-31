import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime

from backend.models import Payment
from backend.models.place import Place

from backend.crud.base import CRUDBase
from backend.models.reservation import Reservation
from backend.schemas.reservation import ReservationCreate


class CRUDReservation(CRUDBase[Reservation, ReservationCreate, ReservationCreate]):
    """
    CRUD operations for the Reservation model.
    """

    @staticmethod
    async def delete_reservation(db: AsyncSession, reservation_id: uuid.UUID) -> Optional[Reservation]:
        """
        Delete a reservation.
        :param db: Database session.
        :param reservation_id: ID of the reservation to delete.
        :return: Deleted Reservation or None.
        """

        reservation = await db.execute(select(Reservation).filter(Reservation.id == reservation_id))
        # db.sync_session.delete(reservation)
        # await db.commit()
        return

    @staticmethod
    async def expired_payment_delete_reservatoin(db: AsyncSession, reservation_id: uuid.UUID) -> Optional[Reservation]:
        """
        Delete a reservation with expired payment.
        :param db: Database session.
        :param reservation_id: ID of the reservation to delete.
        :return: Deleted Reservation or None.
        """

        reservation = await db.execute(select(Reservation).filter(Reservation.id == reservation_id))
        reservation = reservation.scalars().first()

        if not reservation:
            return None

        payment = await db.execute(select(Payment).filter(Payment.id == reservation.payment_id))
        payment = payment.scalar_one_or_none()

        if not payment:
            if (datetime.utcnow() - reservation.created_at).days > 5:
                await db.delete(payment)
                await db.commit()

    @staticmethod
    async def create_reservation(db: AsyncSession, business: str, place: str, fair: str, reservation_in: ReservationCreate) -> Reservation:
        """
        Create a new reservation.
        :param db: Database session.
        :param fair: Fair to create reservation for.
        :param reservation_in: Reservation to create.
        :param business: Business to create reservation for.
        :param place: Place to create reservation for.
        :return: Created Reservation.
        """



        db_reservation = Reservation(
            business_id=reservation_in.business_id,
            fair_id=reservation_in.fair_id,
            payment_id=reservation_in.payment_id,
            place_id=reservation_in.place_id,
        )
        db_reservation.fair = fair
        db_reservation.business = business
        db_reservation.place = place


        db.add(db_reservation)
        await db.commit()
        await db.refresh(db_reservation)
        return db_reservation

reservation_crud = CRUDReservation(Reservation)