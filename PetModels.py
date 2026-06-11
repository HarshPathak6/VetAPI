from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# SQLAlchemy model for storing pet information
class Pet(Base):
    # Database table name
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    species = Column(String)
    breed = Column(String)
    age = Column(Integer)

    owner_name = Column(String)
    owner_phone = Column(String)
    # Timestamp when the pet record was created
    created_at = Column(DateTime, default=datetime.utcnow)

    # One-to-many relationship:
    # One pet can have multiple visits
    # Deleting a pet also deletes all associated visits
    visits = relationship(
    "Visit",
    back_populates="pet",
    cascade="all, delete-orphan",
    passive_deletes=True
)