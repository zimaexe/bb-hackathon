from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
import stripe
from typing import Annotated
from backend.db.session import get_db
from backend.services.auth import get_current_user_email
from backend.crud.fair import fair_crud
from backend.core.config import settings
from backend.schemas.payment import PaymentCreate, PaymentResponse
from backend.services.auth import get_current_user_email
from backend.crud.payment import payment_crud

stripe.api_key = settings.stripe_api_key

router = APIRouter()

@router.post("/pay")
async def process_payment(amount: int, currency: str, token: str, user_email: Annotated[
        str, Security(get_current_user_email)], db: AsyncSession = Depends(get_db)):
    try:
        # charge = stripe.Charge.create(
        #     amount=amount,
        #     currency=currency,
        #     source=token,
        #     description="Payment for place on fair",
        # )

        await payment_crud.create_payment(db=db, payment_in=PaymentCreate(payment_status="success", payment_stripe_id=1), user_email=user_email)

        return {"status": "success", "charge_id": "charge.id"}

    except stripe.error.CardError as e:
        return {"status": "error", "message": str(e)}
    except stripe.error.StripeError as e:
        return {"status": "error", "message": "Something went wrong. Please try again later."}
