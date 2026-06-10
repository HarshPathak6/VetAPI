from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from database import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)

    pet_id = Column(
        Integer,
        ForeignKey("pets.id")
    )

    visit_date = Column(DateTime)

    reason = Column(String)

    notes = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )