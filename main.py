from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from schemas import PetCreate, PetResponse
from crud import create_pet

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Vet API running"}


@app.post("/pets", response_model=PetResponse)
def add_pet(
    pet: PetCreate,
    db: Session = Depends(get_db)
):
    return create_pet(db, pet)
