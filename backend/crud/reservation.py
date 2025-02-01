import uuid
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
from sqlalchemy import or_

from backend.models import Payment
from backend.models.place import Place

from backend.crud.base import CRUDBase
from backend.crud.business import business_crud
from backend.crud.fair import fair_crud
from backend.crud.place import place_crud
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

        reservation = await db.execute(select(Reservation).where(
            Reservation.id == reservation_id))
        reservation = reservation.scalar_one_or_none()
        await CRUDBase.delete(db=db, db_obj=reservation)
        await db.commit()

    @staticmethod
    async def expired_payment_delete_reservatoin(db: AsyncSession) -> Optional[Reservation]:

        reservations = await db.execute(
        select(Reservation)
        .where(
            or_(
                Reservation.payment.has() == False,
                Reservation.payment.has(payment_status="pending")
            ) & ((datetime.now() - Reservation.created_at) > timedelta(days=5))
            ))
        reservations = reservations.scalars().all()

        if not reservations:
            return

        for reservation in reservations:
            await db.delete(reservation)

        await db.commit()

    @staticmethod
    async def get_business_by_reservatoin_id(obj):
        # result = await CRUDReservation.get_by_id(db=db, obj_id=obj_id)

        # if not result:
        #     return

        return obj.business

    @staticmethod
    async def create_reservation(db: AsyncSession, business: str, place: str, fair: str) -> Reservation:
        business = await business_crud.get_by_email(db=db, email=business)
        fair = await fair_crud.get_by_name(db=db, name=fair)
        place = await place_crud.get_place_by_cordinates(db=db, place_cordinates=place)

        if not business or not fair or not place:
            return

        reservation = Reservation()
        reservation.business = business
        reservation.fair = fair
        reservation.place = place

        # business.reservations = reservation
        place.place_reservated = True

        db.add(reservation)

        await db.commit()
        await db.refresh(reservation)
        return reservation

    @staticmethod
    async def is_place_reserved(db: AsyncSession, place_cordinates: str, fair_name: str):
        fair = await fair_crud.get_by_name(db=db, name=fair_name)
        place = await place_crud.get_place_by_cordinates(db=db, place_cordinates=place_cordinates)

        if not fair or not place:
            return

        result = await db.execute(
            select(Reservation).where((Reservation.fair_id == fair.id) & (Reservation.place_id == place.id)))
        result = result.scalar_one_or_none()

        if result:
            return True
        else:
            return False


reservation_crud = CRUDReservation(Reservation)