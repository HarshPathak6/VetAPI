from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from PetModels import Pet
from VisitModels import Visit
from OwnerModels import Owner
from schemas import PetCreate, PetResponse, VisitCreate, VisitResponse, VisitUpdate, OwnerCreate, OwnerResponse
from crud import create_pet, get_pet, get_pets, update_pet, delete_pet, create_visit, get_pet_visits, update_visit, delete_visit



app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Home Page"])
def home():
    return {"message": "Vet API running"}


@app.post(
    "/pets",
    response_model=PetResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Pets"]
)
def add_pet(pet: PetCreate, db: Session = Depends(get_db)):
# Create a new pet record in the database
    return create_pet(db, pet)


@app.get("/pets", response_model=list[PetResponse],tags=["Pets"])
def read_all_pets(db: Session = Depends(get_db)):
# Retrieve all pets stored in the system
    return get_pets(db)

@app.get("/pets/{pet_id}", response_model=PetResponse, tags=["Pets"])
def read_pet(pet_id: int, db: Session = Depends(get_db)):

#Fetch pet by its unique ID
    pet = get_pet(db, pet_id)

#Return 404 if no matching pet exists
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

# Return pet details
    return pet


@app.put("/pets/{pet_id}", response_model=PetResponse, tags=["Pets"])
def edit_pet(
    pet_id: int,
    pet: PetCreate,
    db: Session = Depends(get_db)
):
# Update pet information using supplied data
    updated_pet = update_pet(
        db,
        pet_id,
        pet
    )
# Return error when pet ID does not exist
    if updated_pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )
# Return updated pet record
    return updated_pet


@app.delete("/pets/{pet_id}", status_code=status.HTTP_200_OK, tags=["Pets"])
def remove_pet(
    pet_id: int,
    db: Session = Depends(get_db)
): 
# Attempt to delete the pet from the database
    deleted_pet = delete_pet(db, pet_id)

# Return 404 if the pet does not exist
    if deleted_pet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pet not found"
        )
    
# Return success message after deletion
    return {
        "message": "Pet deleted successfully"
    }

@app.post(
    "/pets/{pet_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Visits"]
)
def add_visit(
    pet_id: int,
    visit: VisitCreate,
    db: Session = Depends(get_db)
):
    
# Check whether the specified pet exists
    pet = get_pet(
        db,
        pet_id
    )

# Prevent creating visits for non-existent pets
    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

# Create and save the visit record
    return create_visit(
        db,
        pet_id,
        visit
    )


@app.get(
    "/pets/{pet_id}/visits",
    response_model=list[VisitResponse],
    tags=["Visits"]
)
def read_visits(
    pet_id: int,
    db: Session = Depends(get_db)
):

# Verify that the pet exists
    pet = get_pet(
        db,
        pet_id
    )

# Return 404 if pet cannot be found
    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

# Return all visits associated with the pet
    return get_pet_visits(
        db,
        pet_id
    )


@app.post("/owners", response_model=OwnerResponse, tags=["Owners"])
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):

    db_owner = Owner(
        name=owner.name,
        phone=owner.phone,
        email=owner.email
    )

    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)

    return db_owner

@app.get("/owners", response_model=list[OwnerResponse], tags=["Owners"])
def get_owners(db: Session = Depends(get_db)):

    return db.query(Owner).all()



@app.put(
    "/visits/{visit_id}",
    response_model=VisitResponse,
    tags=["Visits"]
)
def edit_visit(
    visit_id: int,
    visit: VisitUpdate,
    db: Session = Depends(get_db)
):

    updated_visit = update_visit(
        db,
        visit_id,
        visit
    )

    if updated_visit is None:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    return updated_visit


@app.delete(
    "/visits/{visit_id}",
    tags=["Visits"]
)
def remove_visit(
    visit_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_visit(
        db,
        visit_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    return {
        "message": "Visit deleted successfully"
    }