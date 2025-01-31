from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.crud.base import CRUDBase
from sqlalchemy.future import select
from backend.models.business import Business
from backend.schemas.business import BusinessCreate, BusinessUpdate


class CRUDBusiness(CRUDBase[Business, BusinessCreate, BusinessUpdate]):
    """
    CRUD class for handling Business entities.
    """
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        """
        Retrieve a Business entity by email.
        """
        result = await db.execute(select(Business).filter(Business.email == email))
        return result.scalar_one_or_none()
    @staticmethod
    async def create_business(db: AsyncSession, business_in: BusinessCreate):
        """
        Create a new Business entity and return it.
        """
        db_obj = Business(
            email=business_in.email,
            phone=business_in.phone,
            business_name=business_in.business_name,
            password=Business.hash_password(business_in.password),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def change_business(db: AsyncSession, email:str, admin_in: BusinessCreate):
        admin = await CRUDBusiness.get_by_email(db=db, email=email)
        await CRUDBase.update(db=db, db_obj=admin, obj_in=admin_in)

business_crud = CRUDBusiness(Business)
