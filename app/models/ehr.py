from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class EHR(Base):
    __tablename__ = 'ehrs'
    record_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, index=True)
    diagnosis = Column(String)
    treatment = Column(String)
    notes = Column(String)
    patient = relationship("User", back_populates="ehrs")