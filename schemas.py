from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PetCreate(BaseModel):
    name: str
    species: str
    breed: str
    age: int

    owner_name: str
    owner_phone: str


class PetResponse(BaseModel):
    id: int

    name: str
    species: str
    breed: str
    age: int

    owner_name: str
    owner_phone: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

class VisitCreate(BaseModel):
    visit_date: datetime

    reason: str

    notes: str


class VisitResponse(BaseModel):
    id: int

    pet_id: int

    visit_date: datetime

    reason: str

    notes: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )