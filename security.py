from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from fastapi import Depends, HTTPException, status
from UserModels import User, UserRole
from main import get_current_user

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_receptionist_or_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [
        UserRole.ADMIN.value,
        UserRole.RECEPTIONIST.value
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Receptionist or Admin access required"
        )
    return current_user


def require_vet_or_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [
        UserRole.ADMIN.value,
        UserRole.VET.value
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Veterinarian or Admin access required"
        )
    return current_user