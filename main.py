from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from PetModels import Pet
from VisitModels import Visit
from schemas import PetCreate, PetResponse, VisitCreate, VisitResponse
from crud import create_pet, get_pet, get_pets, update_pet, delete_pet, create_visit, get_pet_visits


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Vet API running"}


@app.post(
    "/pets",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED
)
def add_pet(pet: PetCreate, db: Session = Depends(get_db)):
    return create_pet(db, pet)


@app.get("/pets", response_model=list[PetResponse])
def read_all_pets(db: Session = Depends(get_db)):
    return get_pets(db)

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


@app.delete("/pets/{pet_id}", status_code=status.HTTP_200_OK)
def remove_pet(
    pet_id: int,
    db: Session = Depends(get_db)
):
    deleted_pet = delete_pet(db, pet_id)

    if deleted_pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )

    return {
        "message": "Pet deleted successfully"
    }

@app.post(
    "/pets/{pet_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED
)
def add_visit(
    pet_id: int,
    visit: VisitCreate,
    db: Session = Depends(get_db)
):
    pet = get_pet(
        db,
        pet_id
    )

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    return create_visit(
        db,
        pet_id,
        visit
    )


@app.get(
    "/pets/{pet_id}/visits",
    response_model=list[VisitResponse]
)
def read_visits(
    pet_id: int,
    db: Session = Depends(get_db)
):
    pet = get_pet(
        db,
        pet_id
    )

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    return get_pet_visits(
        db,
        pet_id
    )