from uuid import UUID
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class PlaceBase(BaseModel):
    place_name: str
    place_zona: int
    place_cordinates: str
    place_reservated: bool = False

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(PlaceBase):
    pass

class PlaceResponse(PlaceBase):
    place_id: UUID

    class Config:
        orm_mode = True
