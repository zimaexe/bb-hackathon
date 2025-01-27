from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from schemas.place import PlaceBase

class FairBase(BaseModel):
    name: str
    start_day: datetime
    end_day: datetime
    fair_places: list[PlaceBase]

class FairCreate(FairBase):
    pass

class FairUpdate(FairBase):
    pass

class FairResponse(FairBase):
    fair_id: UUID

    class Config:
        orm_mode = True
