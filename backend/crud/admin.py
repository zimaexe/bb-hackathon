from sqlalchemy.ext.asyncio import AsyncSession
from backend.crud.base import CRUDBase
from sqlalchemy.future import select
from backend.models.admin import Admin
from backend.schemas.admin import AdminCreate, AdminUpdate


class CRUDAdmin(CRUDBase[Admin, AdminCreate, AdminUpdate]):
    """
    CRUD class for handling Admin entities.
    """
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        """
        Retrieve a Business entity by email.
        """
        result = await db.execute(select(Admin).filter(Admin.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_admin(db: AsyncSession, admin_in: AdminCreate):
        """
        Create a new Admin entity and return it.
        """
        db_obj = Admin(
            email=admin_in.email,
            password=Admin.hash_password(password=admin_in.password),
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    @staticmethod
    async def change_admin(db: AsyncSession, admin_in: AdminUpdate):
        admin = await CRUDAdmin.get_by_email(db=db, email=admin_in.email)
        await CRUDBase.update(db=db, db_obj=admin, obj_in=admin_in)



admin_crud = CRUDAdmin(Admin)
