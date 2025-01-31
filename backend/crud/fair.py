from datetime import timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from backend.crud.base import CRUDBase, CreateSchemaType, ModelType
from backend.models.fair import Fair
from backend.schemas.fair import FairCreate, FairUpdate


class CRUDFair(CRUDBase[Fair, FairCreate, FairUpdate]):
    """
    CRUD operations for the Fair model.
    """

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> Optional[Fair]:
        """
        Retrieve a fair by name.
        :param db: Database session.
        :param name: Name of the fair.
        :return: Retrieved Fair or None.
        """
        result = await db.execute(select(Fair).filter(Fair.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_fair(db: AsyncSession, fair_in: "FairCreate") -> "Fair":
        """
        Create a new fair.
        :param db: Database session.
        :param fair_in: Fair to create.
        :return: Created Fair.
        """
        new_fair = Fair(
            name=fair_in.name,
            start_day=fair_in.start_day.replace(tzinfo=None),
            end_day=fair_in.end_day.replace(tzinfo=None),
        )

        db.add(new_fair)
        await db.commit()
        await db.refresh(new_fair)
        return new_fair

    @staticmethod
    async def change_fair(db: AsyncSession, fair_in: "FairCreate") -> "Fair":
        """
        Update an existing fair with new details.
        Args:
            db (AsyncSession): The database session.
            fair_in (FairCreate): The new fair details.
        Returns:
            Fair: The updated fair object, or None if the fair does not exist.
        """


        fair = await CRUDFair.get_by_name(db=db, name=fair_in.name)
        if not fair:
            return

        fair.name = fair_in.name
        fair.start_day = fair_in.start_day.replace(tzinfo=None)
        fair.end_day = fair.end_day.replace(tzinfo=None)

        db.add(fair)

        await db.commit()
        await db.refresh(fair)
        return fair


fair_crud = CRUDFair(Fair)
