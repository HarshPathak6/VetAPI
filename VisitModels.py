from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

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

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    pet = relationship(
    "Pet",
    back_populates="visits"
)