from uuid import UUID
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime

class PaymentClient(BaseModel):
    name: str
    ico: str
    dic: str
    ic_dph: str
    email: EmailStr
    adress: str
    city: str
    zip: str
    phone: PhoneNumber

class PaymentInvoice(BaseModel):
    name: str
    variable: str
    constant: str
    specific: str
    already_paid: bool = False
    invoice_no_formatted: str
    created: datetime
    delivery: datetime
    due: datetime
    comment: str = None

class PaymentItem(BaseModel):
    name: str
    description: str
    quantity: int
    unit: str
    unit_price: float
    tax: float

class PaymentBase(BaseModel):
    payment_client: PaymentClient
    payment_invoice: PaymentInvoice
    payment_item: PaymentItem
    payment_status: str

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    payment_id: UUID
    created_at: datetime
    reservation_id: UUID

    class Config:
        orm_mode = True