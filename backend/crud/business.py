from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.crud.base import BaseCRUD
from backend.models.business import Business
from backend.schemas.business import BusinessCreate, BusinessUpdate

class BusinessCRUD(BaseCRUD[Business, BusinessCreate, BusinessUpdate]):
    """
    BusinessCRUD class for CRUD operations on the Business model.
    """
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Business]:
        """
        Retrieve a business by email address.
        
        Args:
            db (AsyncSession): The database session.
            email (str): The email address of the business.
            
        Returns:
            Optional[Business]: The business with the specified email address, if it exists.
        """
        query = select(Business).where(Business.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_phone(self, db: AsyncSession, phone: str) -> Optional[Business]:
        """
        Retrieve a business by phone number.
        
        Args:
            db (AsyncSession): The database session.
            phone (str): The phone number of the business.
            
        Returns:
            Optional[Business]: The business with the specified phone number, if it exists.
        """
        query = select(Business).where(Business.phone == phone)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_business_name(self, db: AsyncSession, business_name: str) -> Optional[Business]:
        """
        Retrieve a business by business name.
        
        Args:
            db (AsyncSession): The database session.
            business_name (str): The name of the business.
            
        Returns:
            Optional[Business]: The business with the specified business name, if it exists.
        """
        query = select(Business).where(Business.business_name == business_name)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_business(self, db: AsyncSession, obj_in: BusinessCreate) -> Business:
        """
        Create a new business.
        
        Args:
            db (AsyncSession): The database session.
            obj_in (BusinessCreate): The business data to create.

        Returns:
            Business: The newly created business.
            """
        
        db_obj = Business(
            email=obj_in.email,
            business_name=obj_in.business_name,
            phone=obj_in.phone
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    

business = BusinessCRUD()