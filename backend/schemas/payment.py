from uuid import UUID
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from datetime import datetime


class PaymentClient(BaseModel):
    """
    PaymentClient schema for representing payment client information.

    Attributes:
        name (str): The name of the payment client.
        ico (str): The identification number of the payment client.
        dic (str): The tax identification number of the payment client.
        ic_dph (str): The VAT identification number of the payment client.
        email (EmailStr): The email address of the payment client.
        adress (str): The address of the payment client.
        city (str): The city where the payment client is located.
        zip (str): The postal code of the payment client's location.
        phone (PhoneNumber): The phone number of the payment client.
    """

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
    """
    PaymentInvoice represents the schema for a payment invoice.

    Attributes:
        name (str): The name associated with the payment invoice.
        variable (str): The variable symbol for the payment.
        constant (str): The constant symbol for the payment.
        specific (str): The specific symbol for the payment.
        already_paid (bool): Indicates whether the payment has already been made. Defaults to False.
        invoice_no_formatted (str): The formatted invoice number.
        created (datetime): The date and time when the invoice was created.
        delivery (datetime): The date and time when the delivery is scheduled.
        due (datetime): The due date and time for the payment.
        comment (str, optional): Additional comments regarding the payment. Defaults to None.
    """

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
    """
    Represents an item in a payment transaction.

    Attributes:
        name (str): The name of the item.
        description (str): A brief description of the item.
        quantity (int): The quantity of the item.
        unit (str): The unit of measurement for the item.
        unit_price (float): The price per unit of the item.
        tax (float): The tax applied to the item.
    """

    name: str
    description: str
    quantity: int
    unit: str
    unit_price: float
    tax: float


class PaymentBase(BaseModel):
    """
    PaymentBase is a Pydantic model that represents the base schema for a payment.

    Attributes:
        payment_client (PaymentClient): The client associated with the payment.
        payment_invoice (PaymentInvoice): The invoice associated with the payment.
        payment_item (PaymentItem): The item associated with the payment.
        payment_status (str): The status of the payment.
    """

    payment_client: PaymentClient
    payment_invoice: PaymentInvoice
    payment_item: PaymentItem
    payment_status: str


class PaymentCreate(PaymentBase):
    """
    Schema for creating a new payment.

    Inherits from:
        PaymentBase: Base schema for payment-related data.
    """

    pass


class PaymentResponse(PaymentBase):
    """
    PaymentResponse schema for representing payment response data.

    Attributes:
        id (UUID): Unique identifier for the payment.
        created_at (datetime): Timestamp when the payment was created.
        reservation_id (UUID): Unique identifier for the associated reservation.

    Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs.
    """

    id: UUID
    created_at: datetime
    reservation_id: UUID

    class Config:
        from_attributes = True
