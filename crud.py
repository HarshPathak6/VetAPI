from sqlalchemy.orm import Session
from models import Pet
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