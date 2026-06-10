from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    species = Column(String)
    breed = Column(String)
    age = Column(Integer)

    owner_name = Column(String)
    owner_phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)