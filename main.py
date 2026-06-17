#Main.py

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
import time
import logging
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from PetModels import Pet
from VisitModels import Visit
from OwnerModels import Owner
from UserModels import User
from schemas import PetCreate, PetResponse, VisitCreate, VisitResponse, VisitUpdate, OwnerCreate, OwnerResponse, UserResponse, UserCreate, LoginRequest, TokenResponse, UserContextResponse
from crud import create_pet, get_pet, get_pets, update_pet, delete_pet, create_visit, get_pet_visits, update_visit, delete_visit, get_owner_pets
from security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import settings
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    return user


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"Method={request.method} |"
        f"Path={request.url.path} |"
        f"Status={response.status_code} |"
        f"ResponseTime={process_time:.4f}s |"
    )

    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )

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


@app.get(
    "/pets",
    response_model=list[PetResponse],
    tags=["Pets"]
)
def read_all_pets(
    species: str | None = None,
    breed: str | None = None,
    owner_name: str | None = None,
    min_age: int | None = None,
    max_age: int | None = None,
    search: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort_by: str = "id",
    sort_order: str = "asc",
    db: Session = Depends(get_db)
):
    return get_pets(
        db,
        species,
        breed,
        owner_name,
        min_age,
        max_age,
        search,
        page,
        limit,
        sort_by,
        sort_order
    )

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

    pet = get_pet(
        db,
        pet_id
    )

    if pet is None:
        raise HTTPException(
            status_code=404,
            detail="Pet not found"
        )

    visits = get_pet_visits(
        db,
        pet_id
    )

    if not visits:
        raise HTTPException(
            status_code=404,
            detail="No visits found for this pet"
        )

    return visits


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


@app.get(
    "/owners/{owner_id}/pets",
    response_model=list[PetResponse],
    tags=["Owners"]
)
def read_owner_pets(
    owner_id: int,
    db: Session = Depends(get_db)
):

    owner = db.query(Owner).filter(
        Owner.id == owner_id
    ).first()

    if owner is None:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    pets = get_owner_pets(
        db,
        owner_id
    )

    if not pets:
        raise HTTPException(
            status_code=404,
            detail="No pets found for this owner"
        )

    return pets


@app.post(
    "/auth/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    print("PASSWORD:", user.password)
    print("LENGTH:", len(user.password))
    hashed_password = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role.value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post(
    "/auth/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
    User.email == form_data.username
).first()

    if not user or not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get(
    "/auth/user-context",
    response_model=UserContextResponse,
    tags=["Authentication"]
)
def get_user_context(
    current_user: User = Depends(get_current_user)
):
    return current_user


