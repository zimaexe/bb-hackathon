import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.crud.base import CRUDBase
from backend.models.reservation import Reservation
from backend.schemas.reservation import ReservationCreate


class CRUDReservation(CRUDBase[Reservation, ReservationCreate, ReservationCreate]):
    """
    CRUD operations for the Reservation model.
    """

    @staticmethod
    @staticmethod
    async def create_reservation(
        db: AsyncSession, reservation_in: ReservationCreate
    ) -> Reservation:
        """
        Create a new reservation.
        :param db: Database session.
        :param fair: Fair to create reservation for.
        :param reservation_in: Reservation to create.
        :param business: Business to create reservation for.
        :param place: Place to create reservation for.
        :return: Created Reservation.
        """

        existing_reservation = await db.execute(
            select(Reservation).where(
                Reservation.fair_id == reservation_in.fair_id,
                Reservation.place_id == reservation_in.place_id,
            )
        )
        if existing_reservation.scalars().first():
            raise ValueError("This place is already reserved for the given fair.")

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
