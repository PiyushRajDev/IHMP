from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.models.enums import StatusEnum

class Appointment(Base):
    __tablename__ = 'appointments'
    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('users.user_id'))
    doctor_id = Column(Integer, ForeignKey('users.user_id'))
    appointment_date = Column(DateTime)
    status = Column(Enum(StatusEnum), nullable=False)
    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="appointments_as_doctor")