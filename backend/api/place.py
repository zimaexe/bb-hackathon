from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.schemas.place import PlaceCreate, PlaceResponse, PlaceUpdate
from backend.crud.place import place_crud
from backend.crud.fair import fair_crud
from backend.db.session import get_db

router = APIRouter()


@router.post("/create_place", response_model=PlaceResponse, status_code=status.HTTP_200_OK)
async def create_place(place: PlaceCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new place.
    This function creates a new place in the database. It first checks if a place with the same coordinates already exists.
    If such a place exists, it logs an error and raises an HTTP 400 exception. If the place does not exist, it attempts to
    create the place and handle any exceptions that may occur during the process.
    Args:
        place (PlaceCreate): The place data to be created.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(get_db).
    Returns:
        The created place.
    Raises:
        HTTPException: If a place with the same coordinates already exists (HTTP 400).
        HTTPException: If an error occurs during the creation process (HTTP 500).
    """

    db_fair = await place_crud.get_place_by_cordinates(db=db, name=place.place_cordinates)
    if db_fair:
        logger.error(
            f"Error creating place: Place with cordinates {place.place_cordinates} already exist."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Place cordinates already registered.",
        )
    try:
        place = await place_crud.create_place(db=db, place=place)
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong.",
        )
    return place


@router.post("/add_place_to_fair", response_model=PlaceResponse, status_code=status.HTTP_202_ACCEPTED)
async def add_place_fair(place_cordinates: str, fair_name: str, db: AsyncSession = Depends(get_db)):
    """
    Asynchronously adds a fair to a place based on provided coordinates and fair name.
    Args:
        place_cordinates (str): The coordinates of the place where the fair will be added.
        fair_name (str): The name of the fair to be added.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(get_db).
    Raises:
        HTTPException: If the place with the given coordinates or the fair with the given name is not found.
    Returns:
        The result of adding the fair to the place.
    """

    place = place_crud.get_place_by_cordinates(db=db, place_cordinates=place_cordinates)
    fair = fair_crud.get_by_name(db=db, name=fair_name)

    if not place or not fair:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place with cordinates or fair with name was not found")

    return await place_crud.add_fair_to_place(db=db, place_cordinates=place_cordinates, fair=fair)

@router.post("/remove_place_from_fair", response_model=PlaceResponse, status_code=status.HTTP_202_ACCEPTED)
async def add_place_fair(place_cordinates: str, fair_name: str, db: AsyncSession = Depends(get_db)):
    """
    Asynchronously adds a fair to a place based on provided coordinates and fair name.
    Args:
        place_cordinates (str): The coordinates of the place where the fair will be added.
        fair_name (str): The name of the fair to be added to the place.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(get_db).
    Raises:
        HTTPException: If the place with the given coordinates or the fair with the given name is not found.
    Returns:
        The result of removing the fair from the place.
    """

    place = place_crud.get_place_by_cordinates(db=db, place_cordinates=place_cordinates)
    fair = fair_crud.get_by_name(db=db, name=fair_name)

    if not place or not fair:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place with cordinates or fair with name was not found")

    return await place_crud.remove_fair_from_place(db=db, place_cordinates=place_cordinates, fair=fair)