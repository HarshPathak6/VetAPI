from sqlalchemy.orm import Session
from PetModels import Pet
from schemas import PetCreate


def create_pet(db: Session, pet: PetCreate):
    db_pet = Pet(
        name=pet.name,
        species=pet.species,
        breed=pet.breed,
        age=pet.age,
        owner_name=pet.owner_name,
        owner_phone=pet.owner_phone
    )

    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)

    return db_pet

def get_pet(db: Session, pet_id: int):
    return db.query(Pet).filter(Pet.id == pet_id).first()

def update_pet(db: Session, pet_id: int, pet_data: PetCreate):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if pet is None:
        return None

    pet.name = pet_data.name
    pet.species = pet_data.species
    pet.breed = pet_data.breed
    pet.age = pet_data.age
    pet.owner_name = pet_data.owner_name
    pet.owner_phone = pet_data.owner_phone

    db.commit()
    db.refresh(pet)

    return pet


def delete_pet(db: Session, pet_id: int):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()

    if pet is None:
        return None

    db.delete(pet)
    db.commit()

    return pet
    