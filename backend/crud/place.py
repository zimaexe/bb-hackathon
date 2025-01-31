from typing import List, Optional
from pydantic import EmailStr
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import exists

from backend.crud.base import CRUDBase
from backend.models.place import Place
from backend.schemas.place import PlaceCreate, PlaceUpdate
from backend.models.fair import Fair

class CRUDPlace(CRUDBase[Place, PlaceCreate, PlaceUpdate]):
    """
    CRUD operations for the Place model.
    """

    @staticmethod
    async def create_place(db: AsyncSession, place: "PlaceCreate") -> "Place":
        """
        Create a new place in the database.
        Args:
            db (AsyncSession): The database session.
            place (PlaceCreate): The place data to create.
        Returns:
            Place: The newly created place.
        """

        db_place = Place(
            place_name = place.place_name,
            place_zona = place.place_zona,
            place_cordinates = place.place_cordinates,
            place_reservated = place.place_reservated,
            fairs = []
        )
        db.add(db_place)
        await db.commit()
        await db.refresh(db_place)
        return db_place

    @staticmethod
    async def get_place_by_cordinates(db: AsyncSession, place_cordinates: str) -> "Place":
        """
        Retrieve a Place object from the database based on its coordinates.
        Args:
            db (AsyncSession): The database session to use for the query.
            place_cordinates (str): The coordinates of the place to retrieve.
        Returns:
            Place: The Place object if found, otherwise None.
        """

        result = await db.execute(select(Place).where(Place.place_cordinates == place_cordinates))
        return result.scalar_one_or_none()

    @staticmethod
    async def add_fair_to_place(db: AsyncSession, place_cordinates: str, fair: "Fair") -> "Place":
        """
        Adds a fair to a place identified by its coordinates.
        Args:
            db (AsyncSession): The database session.
            place_cordinates (str): The coordinates of the place.
            fair (Fair): The fair to be added to the place.
        Returns:
            Place: The updated place with the new fair added.
        Raises:
            Exception: If the place with the given coordinates is not found.
        """

        place = await CRUDPlace.get_place_by_cordinates(db=db, place_cordinates=place_cordinates)
        await db.run_sync(lambda sync_session: place.fairs.append(fair))
        db.add(place)

        await db.commit()
        await db.refresh(place)
        return place

    @staticmethod
    async def remove_fair_from_place(db: AsyncSession, place_cordinates: str, fair: "Fair") -> "Place":
        """
        Remove a fair from a place based on the place coordinates.
        Args:
            db (AsyncSession): The database session.
            place_cordinates (str): The coordinates of the place.
            fair (Fair): The fair to be removed from the place.
        Returns:
            Place: The updated place object with the fair removed.
        Raises:
            Exception: If the place with the given coordinates is not found.
        """

        place = await CRUDPlace.get_place_by_cordinates(db=db, place_cordinates=place_cordinates)
        await db.run_sync(lambda sync_session: place.fairs.remove(fair))
        db.add(place)

        await db.commit()
        await db.refresh(place)
        return place

place_crud = CRUDPlace(Place)
