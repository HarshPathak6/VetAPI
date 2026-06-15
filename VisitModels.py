# VisitModels.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

# SQLAlchemy model for storing veterinary visit records
class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking visit to a pet
    # CASCADE ensures visits are removed when the pet is deleted
    pet_id = Column(
    Integer,
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