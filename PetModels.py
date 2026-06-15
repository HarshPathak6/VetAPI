from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
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

    owner_id = Column(Integer, ForeignKey("owners.id"))
    owner = relationship("Owner", back_populates="pets")
    # Timestamp when the pet record was created
    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    is_deleted = Column(
        Boolean,
        default=False
    )

    deleted_at = Column(
        DateTime,
        nullable=True,
    )
    # One-to-many relationship:
    # One pet can have multiple visits
    # Deleting a pet also deletes all associated visits
    visits = relationship(
    "Visit",
    back_populates="pet",
    cascade="all, delete-orphan",
    passive_deletes=True
)
    
