from datetime import datetime
from pydantic import BaseModel, ConfigDict

# Request schema used when creating or updating a pet
class PetCreate(BaseModel):
    name: str
    species: str
    breed: str
    age: int

    owner_name: str
    owner_phone: str

# Response schema returned by pet-related endpoints
class PetResponse(BaseModel):
    id: int

    name: str
    species: str
    breed: str
    age: int

    owner_name: str
    owner_phone: str

    created_at: datetime

    # Allows conversion from SQLAlchemy objects to Pydantic models
    model_config = ConfigDict(from_attributes=True)

    
# Request schema used when creating a visit record
class VisitCreate(BaseModel):
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

    # Allows conversion from SQLAlchemy objects to Pydantic models
    model_config = ConfigDict(
        from_attributes=True
    )