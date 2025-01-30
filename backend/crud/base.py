from typing import Generic, Type, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.base import BaseModel


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new object in the database
        :param db: AsyncSession
        :param obj_in: CreateSchemaType
        :return: ModelType
        """
        
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    async def get_by_id(self, db: AsyncSession, obj_id: int) -> Optional[ModelType]:
        """
        Get an object by ID
        :param db: AsyncSession
        :param id: int
        :return: Optional[ModelType]
        """
        
        query = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession) -> List[ModelType]:
        """
        Get all objects
        :param db: AsyncSession
        :return: List[ModelType]
        """
        
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, obj_id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        """
        Update an object by ID
        :param db: AsyncSession
        :param id: int
        :param obj_in: UpdateSchemaType
        :return: Optional[ModelType]
        """
        
        query = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(query)
        db_obj = result.scalar_one_or_none()
        if db_obj:
            obj_data = obj_in.dict(exclude_unset=True)
            for key, value in obj_data.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, obj_id: int) -> Optional[ModelType]:
        """
        Delete an object by ID
        :param db: AsyncSession
        :param id: int
        :return: Optional[ModelType]
        """
        
        query = select(self.model).where(self.model.id == obj_id)
        result = await db.execute(query)
        db_obj = result.scalar_one_or_none()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj