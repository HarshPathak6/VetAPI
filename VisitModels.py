# VisitModels.py

from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import UUID

# SQLAlchemy model for storing veterinary visit records
class Visit(Base):
    __tablename__ = "visits"

    id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid4,
    index=True
)
    # Foreign key linking visit to a pet
    # CASCADE ensures visits are removed when the pet is deleted
    pet_id = Column(
    UUID(as_uuid=True),
    ForeignKey(
        "pets.id",
        ondelete="CASCADE"
    )
)

    visit_date = Column(DateTime)

    reason = Column(String)

    notes = Column(String)

    # Timestamp when the visit record was created
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Many-to-one relationship:
    # Multiple visits can belong to one pet
    pet = relationship(
    "Pet",
    back_populates="visits"
)
    
    updated_at = Column(
    DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)