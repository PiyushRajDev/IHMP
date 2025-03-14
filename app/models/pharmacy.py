from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.database import Base

class Pharmacy(Base):
    __tablename__ = 'pharmacys'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
