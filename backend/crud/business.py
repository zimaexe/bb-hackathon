from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.base import CRUDBase
from backend.models.business import Business
from backend.schemas.business import BusinessCreate, BusinessUpdate


class CRUDBusiness(CRUDBase[Business, BusinessCreate, BusinessUpdate]):
    """
    CRUD class for handling Business entities.
    """

    async def create_business(self, db: AsyncSession, business_in: BusinessCreate):
        """
        Create a new Business entity and return it.
        """
        db_obj = Business(
            email=business_in.email,
            phone=business_in.phone,
            business_name=business_in.business_name,
            password=business_in.password
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj



business_crud = CRUDBusiness(Business)