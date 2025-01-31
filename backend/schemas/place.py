from uuid import UUID
from pydantic import BaseModel


class PlaceBase(BaseModel):
    """
    PlaceBase is a Pydantic model that represents the basic information of a place.

    Attributes:
        place_name (str): The name of the place.
        place_zona (int): The zone number of the place.
        place_cordinates (str): The coordinates of the place.
        place_reservated (bool): Indicates whether the place is reserved. Defaults to False.
    """

    place_name: str
    place_zona: int
    place_cordinates: str
    place_reservated: bool = False


class PlaceCreate(PlaceBase):
    """
    PlaceCreate schema for creating a new place.

    This class inherits from PlaceBase and does not add any additional fields or methods.
    """

    pass


class PlaceUpdate(PlaceBase):
    """
    PlaceUpdate schema for updating place information.

    This class inherits from PlaceBase and does not add any additional fields or methods.
    It is used to validate and handle data when updating an existing place.
    """

    pass


class PlaceResponse(PlaceBase):
    """
    PlaceResponse schema for representing a place with an ID.

    Attributes:
        id (UUID): Unique identifier for the place.

    Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs like SQLAlchemy.
    """

    id: UUID

    class Config:
        from_attributes = True
