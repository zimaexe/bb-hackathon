from typing import Generic, List, Optional, TypeVar

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD class for basic operations.
    """

    def __init__(self, model: ModelType):
        self.model = model

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new object.
        :param db: Database session.
        :param obj_in: Object to create.
        :return: Object created.
        """
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, obj_id: int) -> Optional[ModelType]:
        """
        Get an object by ID.
        """
        query = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        """
        Get all objects.
        :param db: Database session.
        :return: List of all objects.
        """
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update(
        db: AsyncSession, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update an object.
        :param db: Database session.
        :param db_obj: Database object to update.
        :param obj_in: Data to update.
        :return: Updated object.
        """
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def delete(db: AsyncSession, db_obj: ModelType) -> None:
        """
        Delete an object.
        :param db: Database session.
        :param db_obj: Database object to delete.
        :return: None
        """
        await db.delete(db_obj)
        await db.commit()
