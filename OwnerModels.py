from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship



class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    Created_at = Column(DateTime, default=datetime.utcnow)

    pets = relationship("Pet", back_populates="owner")