from uuid import UUID
from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    """
    AdminBase schema for representing basic admin information.

    Attributes:
        email (EmailStr): The email address of the admin.
        admin_name (str): The name of the admin.
    """

    email: EmailStr


class AdminCreate(AdminBase):
    """
    AdminCreate schema for creating a new admin.

    Attributes:
        password (str): The password for the admin account.
    """

    password: str


class AdminUpdate(AdminCreate):
    """
    AdminUpdate schema for updating an existing admin.

    This class inherits from AdminCreate and does not add any additional fields
    or methods. It is used to distinguish between creating a new admin and
    updating an existing one.
    """

    pass


class AdminResponse(AdminBase):
    """
    AdminResponse schema for representing an admin entity response.

    Attributes:
        id (UUID): Unique identifier for the admin.

    Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs.
    """

    id: UUID

    class Config:
        from_attributes = True
