from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.database import Base

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
