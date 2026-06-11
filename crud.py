from sqlalchemy.orm import Session
from PetModels import Pet
from schemas import PetCreate, VisitCreate
from VisitModels import Visit

def create_pet(db: Session, pet: PetCreate):
    # Create a new Pet model instance using request data
    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        breed=pet.breed,
        age=pet.age,
        owner_name=pet.owner_name,
        owner_phone=pet.owner_phone
    )

    #Add the pet to the current database session
    db.add(db_pet)
    # Save changes permanently to the database
    db.commit()
    #Reload object to get generated values such as ID
    db.refresh(db_pet)

    return db_pet

def get_pets(db: Session):
    #Retrieve all pets from the database
    return db.query(Pet).all()

def get_pet(db: Session, pet_id: int):
    #Search for a pet using its unique ID
    return db.query(Pet).filter(Pet.id == pet_id).first()

def update_pet(db: Session, pet_id: int, pet_data: PetCreate):
    # Find the pet that needs to be updated
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    #Return None if pet does not exist
    if pet is None:
        return None

    #Update pet details with new values
    pet.name = pet_data.name
    pet.species = pet_data.species
    pet.breed = pet_data.breed
    pet.age = pet_data.age
    pet.owner_name = pet_data.owner_name
    pet.owner_phone = pet_data.owner_phone

    #Save updated information
    db.commit()
    #Reload updated object from database
    db.refresh(pet)

    return pet


def delete_pet(db: Session, pet_id: int):
    #Locate pet before attempting deletion
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    #Return None if pet cannot be found
    if pet is None:
        return None

    #Delete pet and associated visits through cascade rules
    db.delete(pet)
    #Commit deletion to database
    db.commit()

    return pet
    
def create_visit(
    db: Session,
    pet_id: int,
    visit_data: VisitCreate
):
    # Create a visit linked to the specified pet
    db_visit = Visit(
        pet_id=pet_id,
        visit_date=visit_data.visit_date,
        reason=visit_data.reason,
        notes=visit_data.notes
    )

    # Add visit record to database session
    db.add(db_visit)
    # Save visit record
    db.commit()
    # Reload object to obtain generated values
    db.refresh(db_visit)

    return db_visit


def get_pet_visits(
    db: Session,
    pet_id: int
):
    # Retrieve all visits associated with a specific pet
    return (
        db.query(Visit)
        .filter(
            Visit.pet_id == pet_id
        )
        .all()
    )