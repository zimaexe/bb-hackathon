from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class FairBase(BaseModel):
    """
    FairBase schema for representing a fair event.

    Attributes:
        name (str): The name of the fair.
        start_day (datetime): The starting date and time of the fair.
        end_day (datetime): The ending date and time of the fair.
        fair_places (list[PlaceBase]): A list of places associated with the fair.
    """

    name: str
    start_day: datetime
    end_day: datetime
    # fair_places: list[PlaceBase]


class FairCreate(FairBase):
    """
    FairCreate schema for creating a new fair.

    This class inherits from FairBase and currently does not add any additional
    attributes or methods. It is used to define the structure of data required
    to create a new fair.
    """

    pass


class FairUpdate(FairBase):
    """
    FairUpdate schema for updating Fair entities.

    This class inherits from FairBase and is used to define the schema for updating
    existing Fair entities. Currently, it does not add any additional fields or
    methods to the base schema.
    """

    pass


class FairResponse(FairBase):
    """
    FairResponse schema for representing a fair entity response.

    Attributes:
        id (UUID): Unique identifier for the fair.

    Config:
        orm_mode (bool): Enables ORM mode for compatibility with ORMs.
    """

    id: UUID


    class Config:
        from_attributes = True
