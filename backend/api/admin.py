from fastapi import APIRouter, Depends, HTTPException, status

from backend.db.session import get_db
from backend.crud.admin import admin_crud
from backend.schemas.admin import AdminCreate, AdminResponse


router = APIRouter()


@router.post("/", response_model=AdminResponse, status_code=status.HTTP_201_CREATED)
async def create_admin(
        admin_in: AdminCreate, db=Depends(get_db)
) -> AdminResponse:
    """
    Create a new admin.
    """

    try:
        admin = await admin_crud.create_admin(db, admin_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return admin
