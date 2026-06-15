#schemas.py

from datetime import datetime
from pydantic import BaseModel, ConfigDict

# Request schema used when creating or updating a pet
class PetCreate(BaseModel):
    name: str
    species: str
    breed: str
    age: int

    owner_id: int

# Response schema returned by pet-related endpoints
class PetResponse(BaseModel):
    id: int

    name: str
    species: str
    breed: str
    age: int

    owner_id: int

    created_at: datetime

    updated_at: datetime

is_deleted: bool

deleted_at: datetime | None = None
    
# Allows conversion from SQLAlchemy objects to Pydantic models
model_config = ConfigDict(from_attributes=True)


# Request schema used when creating a visit record
class VisitCreate(BaseModel):
    visit_date: datetime

    reason: str

    notes: str

class VisitUpdate(BaseModel):
    visit_date: datetime
    reason: str
    notes: str
    
# Response schema returned by visit-related endpoints
class VisitResponse(BaseModel):
    id: int

    pet_id: int

    visit_date: datetime

    reason: str

    notes: str

    created_at: datetime
    updated_at: datetime

    # Allows conversion from SQLAlchemy objects to Pydantic models
    model_config = ConfigDict(
        from_attributes=True
    )

class OwnerCreate(BaseModel):
    name: str
    phone: str
    email: str

class OwnerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    created_at: datetime


    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)