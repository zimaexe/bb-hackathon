from sqlalchemy.ext.asyncio import AsyncSession
from  backend.crud.base import CRUDBase

from backend.models.admin import Admin
from backend.schemas.admin import AdminCreate, AdminUpdate


class CRUDAdmin(CRUDBase[Admin, AdminCreate, AdminUpdate]):
    """
    CRUD class for handling Admin entities.
    """

    async def create_admin(self, db: AsyncSession, admin_in: AdminCreate):
        """
        Create a new Admin entity and return it.
        """
        db_obj = Admin(
            email=admin_in.email,
            password=admin_in.password
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

admin_crud = CRUDAdmin(Admin)