from sqlalchemy.orm import Session
from PetModels import Pet
from schemas import PetCreate, VisitCreate
from VisitModels import Visit
from OwnerModels import Owner
from sqlalchemy import asc, desc
from datetime import datetime


def create_pet(db: Session, pet: PetCreate):
    # Create a new Pet model instance using request data
    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        breed=pet.breed,
        age=pet.age,
        owner_id=pet.owner_id
    )

    #Add the pet to the current database session
    db.add(db_pet)
    # Save changes permanently to the database
    db.commit()
    #Reload object to get generated values such as ID
    db.refresh(db_pet)

    return db_pet

def get_pets(
    db: Session,
    species=None,
    breed=None,
    owner_name=None,
    min_age=None,
    max_age=None,
    search=None,
    page=1,
    limit=10,
    sort_by="id",
    sort_order="asc"
):
    query = db.query(Pet).filter(
    Pet.is_deleted == False
)

    # Search by pet name
    if search:
        query = query.filter(
            Pet.name.ilike(f"%{search}%")
        )

    # Filter by species
    if species:
        query = query.filter(
            Pet.species == species
        )

    # Filter by breed
    if breed:
        query = query.filter(
            Pet.breed == breed
        )

    # Filter by owner name
    if owner_name:
        query = (
            query.join(Owner)
            .filter(
                Owner.name.ilike(f"%{owner_name}%")
            )
        )

    # Minimum age
    if min_age is not None:
        query = query.filter(
            Pet.age >= min_age
        )

    # Maximum age
    if max_age is not None:
        query = query.filter(
            Pet.age <= max_age
        )

    # Sorting
    allowed_fields = {
        "name": Pet.name,
        "age": Pet.age,
        "created_at": Pet.created_at,
        "id": Pet.id
    }

    sort_column = allowed_fields.get(
        sort_by,
        Pet.id
    )

    if sort_order.lower() == "desc":
        query = query.order_by(
            desc(sort_column)
        )
    else:
        query = query.order_by(
            asc(sort_column)
        )

    # Pagination
    offset = (page - 1) * limit

    query = query.offset(offset).limit(limit)

    return query.all()

def get_pet(db: Session, pet_id: int):
    #Search for a pet using its unique ID
    return db.query(Pet).filter(
    Pet.id == pet_id,
    Pet.is_deleted == False
    ).first()

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
    pet.owner_id = pet_data.owner_id

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

    pet.is_deleted = True
    pet.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(pet)

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

def update_visit(db, visit_id, visit_data):

    visit = db.query(Visit).filter(

        Visit.id == visit_id
    ).first()

    if visit is None:
        return None
    
    visit.visit_date = visit_data.visit_date
    visit.reason = visit_data.reason
    visit.notes = visit_data.notes

    db.commit()
    db.refresh(visit)

    return visit

def delete_visit(db, visit_id):

    visit = db.query(Visit).filter(
        Visit.id == visit_id
    ).first()

    if visit is None:
        return False

    db.delete(visit)
    db.commit()

    return True