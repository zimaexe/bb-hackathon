from uuid import UUID
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime

class ReservationBase(BaseModel):
    business_id: UUID
    fair_id: UUID
    place_id: UUID
    reserved_date: datetime
    payment_status: str

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    reservation_id: UUID

    class Config:
        orm_mode = True
