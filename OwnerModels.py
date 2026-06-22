#OwnerModels.py

from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship



class Owner(Base):
    __tablename__ = "owners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pets = relationship("Pet", back_populates="owner")

    updated_at = Column(
    DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)
    
