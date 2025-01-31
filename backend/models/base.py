import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Column, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


# @as_declarative()
class BaseModel(DeclarativeBase):
    """
    Base model for all database tables. Includes common fields such as
    id, created_at, and updated_at.
    """

    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


# Many-to-Many Association Table for Fair <-> Place
fair_place_association = Table(
    "fair_place_association",
    BaseModel.metadata,
    Column("fair_id", UUID, ForeignKey("fair.id")),
    Column("place_id", UUID, ForeignKey("place.id")),
)
