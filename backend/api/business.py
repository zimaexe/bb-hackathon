from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from loguru import logger

from backend.db.session import get_db
from backend.crud.business import business_crud
from backend.schemas.business import BusinessCreate, BusinessResponse

router = APIRouter()


@router.post("/", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
async def create_business(
        business_in: BusinessCreate, db: AsyncSession = Depends(get_db)
) -> BusinessResponse:
    """
    Create a new business.
    """

    try:
        business = await business_crud.create_business(db, business_in)
        logger.info(f"Business created successfully: {business}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong1.",
        )
    return business
