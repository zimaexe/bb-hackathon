from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.crud.base import BaseCRUD
from backend.models.place import Place
from backend.schemas.place import PlaceCreate, PlaceUpdate


class PlaceCRUD(BaseCRUD[Place, PlaceCreate, PlaceUpdate]):
    """
    PlaceCRUD class for CRUD operations on the Place model.
    """

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Place]:
        """
        Retrieve a place by name.

        Args:
            db (AsyncSession): The database session.
            name (str): The name of the place.

        Returns:
            Optional[Place]: The place with the specified name, if it exists.
        """
        query = select(Place).where(Place.place_name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_place_zona(self, db: AsyncSession, place_zona: int) -> List[Place]:
        """
        Retrieve all places in a specific zone.

        Args:
            db (AsyncSession): The database session.
            place_zona (int): The zone number.

        Returns:
            List[Place]: A list of all places in the specified zone.
        """
        query = select(Place).where(Place.place_zona == place_zona)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_coordinates(self, db: AsyncSession, coordinates: str) -> Optional[Place]:
        """
        Retrieve a place by coordinates.

        Args:
            db (AsyncSession): The database session.
            coordinates (str): The coordinates of the place.

        Returns:
            Optional[Place]: The place with the specified coordinates, if it exists.
        """
        query = select(Place).where(Place.place_cordinates == coordinates)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, db, obj_in):
        """
        Create a new place.

        Args:
            db (AsyncSession): The database session.
            obj_in (PlaceCreate): The data for the new place.

        Returns:
            Place: The newly created place.
        """
        obj = Place(**obj_in.dict())
        db.add(obj)
        await db.commit()
        return obj