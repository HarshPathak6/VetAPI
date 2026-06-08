from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from schemas import PetCreate, PetResponse
from crud import create_pet, get_pet, get_pet, update_pet, delete_pet

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Vet API running"}


@app.post("/pets", response_model=PetResponse)
def add_pet(pet: PetCreate, db: Session = Depends(get_db)):
    return create_pet(db, pet)


@app.get("/pets/{pet_id}", response_model=PetResponse)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = get_pet(db, pet_id)

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    return pet

@app.put("/pets/{pet_id}", response_model=PetResponse)
def edit_pet(
    pet_id: int,
    pet: PetCreate,
    db: Session = Depends(get_db)
):
    updated_pet = update_pet(
        db,
        pet_id,
        pet
    )

    if updated_pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    return updated_pet
