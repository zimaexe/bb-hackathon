from uuid import UUID
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class BusinessBase(BaseModel):
    email: EmailStr
    phone: PhoneNumber
    business_name: str

class BusinessCreate(BusinessBase):
    password: str

class BusinessUpdate(BusinessCreate):
    business_id: UUID

    class Config:
        orm_mode = True


class BusinessResponse(BusinessBase):
    business_id: UUID

