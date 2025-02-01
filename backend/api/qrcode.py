import io
import qrcode
from typing import Annotated
from backend.services.auth import get_current_user_email
from fastapi import APIRouter, Security, Depends, HTTPException
from starlette.responses import StreamingResponse
from backend.crud.business import business_crud
from backend.db.session import AsyncSession, get_db
router = APIRouter()

@router.get("/generate_qr_code")
async def generate(user_email: Annotated[
        str, Security(get_current_user_email)
    ], db: AsyncSession = Depends(get_db)):
    reservation_id = await business_crud.get_reservation_id(db=db, email=user_email)
    if not reservation_id:
        raise HTTPException(status_code=404, detail="reservation was not found")
    message = "0.0.0.0/get_reservation/" + str(reservation_id)
    img = qrcode.make(message)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0) # important here!
    return StreamingResponse(buf, media_type="image/jpeg")
