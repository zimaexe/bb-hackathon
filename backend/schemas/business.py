from uuid import UUID
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class BusinessBase(BaseModel):
    """
    BusinessBase schema for representing basic business information.

    Attributes:
        email (EmailStr): The email address of the business.
        phone (PhoneNumber): The phone number of the business.
        business_name (str): The name of the business.
    """

    email: EmailStr
    phone: str
    business_name: str


class BusinessCreate(BusinessBase):
    """
    BusinessCreate schema for creating a new business.

    Attributes:
        password (str): The password for the business account.
    """

    password: str


class BusinessUpdate(BusinessCreate):
    """
    BusinessUpdate schema for updating an existing business.

    This class inherits from BusinessCreate and does not add any additional fields
    or methods. It is used to distinguish between creating a new business and
    updating an existing one.
    """

    pass


class BusinessResponse(BusinessBase):
    """
    BusinessResponse schema for representing a business entity response.

    Attributes:
        id (UUID): Unique identifier for the business.

    Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs.
    """

    id: UUID

    class Config:
        orm_mode = True
