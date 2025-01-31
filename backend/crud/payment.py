from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.crud.base import CRUDBase
from backend.models.payment import Payment
from backend.crud.business import business_crud
from backend.schemas.payment import PaymentCreate, PaymentBase
from backend.models.fair import Fair


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentCreate]):
    """
    CRUD operations for the Place model.
    """

    @staticmethod
    async def create_payment(db: AsyncSession, payment_in: "PaymentCreate", user_email: str) -> "PaymentBase":
        """
        Create a new place in the database.
        Args:
            db (AsyncSession): The database session.
            place (PlaceCreate): The place data to create.
        Returns:
            Place: The newly created place.
        """

        pay = Payment(
            payment_status=payment_in.payment_status,
            payment_stripe_id=payment_in.payment_stripe_id
        )
        business = (await business_crud.get_by_email(db=db, email=user_email))

        if not business:
            return
        try:
            reservation = business.reservations[-1]
        except:
            return
        reservation.payment = pay
        db.add(reservation)
        await db.commit()
        await db.refresh(pay)
        return pay



payment_crud = CRUDPayment(Payment)
