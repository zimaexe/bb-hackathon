from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel


class Payment(BaseModel):
    """
    Represents a payment model in the database.
    Attributes:
        __tablename__ (str): The name of the table in the database.
        payment_status (Mapped[str]): The status of the payment, defaults to "pending".
        reservation (relationship): A one-to-one relationship with the Reservation model.
    """


    __tablename__ = "payment"
    payment_status: Mapped[str] = mapped_column(default="pendign")
    # 1:1 with Reservation
    reservation = relationship("Reservation", back_populates="payment", uselist=False)

