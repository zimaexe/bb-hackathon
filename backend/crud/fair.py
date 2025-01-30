from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.crud.base import BaseCRUD
from backend.models.fair import Fair
from backend.schemas.fair import FairCreate, FairUpdate

class FairCRUD(BaseCRUD[Fair, FairCreate, FairUpdate]):
    """
    FairCRUD class for CRUD operations on the Fair model.
    """

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Fair]:
        """
        Retrieve a fair by name.

        Args:
            db (AsyncSession): The database session.
            name (str): The name of the fair.

        Returns:
            Optional[Fair]: The fair with the specified name, if it exists.
        """
        query = select(Fair).where(Fair.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    
    async def create(self, db, obj_in):
        """
        Create a new fair.

        Args:
            db (AsyncSession): The database session.
            obj_in (FairCreate): The data for the new fair.

        Returns:
            Fair: The newly created fair.
        """
        obj = Fair(**obj_in.dict())
        db.add(obj)
        await db.commit()
        return obj