from datetime import datetime
from sqlalchemy import Column, Date, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
from app.database.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.database.database import Base

Base = declarative_base()

# Enums
class RoleEnum(str, enum.Enum):
    Doctor = "Doctor"
    Patient = "Patient"
    Admin = "Admin"

class StatusEnum(str, enum.Enum):
    Scheduled = "Scheduled"
    Completed = "Completed"
    Cancelled = "Cancelled"

# Models
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone_number = Column(String(20))
    role = Column(Enum(RoleEnum), nullable=False)
    appointments_as_patient = relationship("Appointment", foreign_keys="[Appointment.patient_id]", back_populates="patient")
    allergies = relationship("AllergyTracking", back_populates="user")
    appointments_as_doctor = relationship("Appointment", foreign_keys="[Appointment.doctor_id]", back_populates="doctor")


class EHR(Base):
    __tablename__ = 'ehr'
    record_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    diagnosis = Column(Text, nullable=False)
    treatment = Column(Text, nullable=False)
    notes = Column(Text)


class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    doctor_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default="Scheduled")
    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")
    doctor = relationship("User", foreign_keys=[doctor_id], back_populates="appointments_as_doctor")


class AllergyTracking(Base):
    __tablename__ = 'allergy_tracking'
    allergy_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    allergy_name = Column(String(100), nullable=False)
    reaction = Column(String(200), nullable=True)
    user = relationship("User", back_populates="allergies")

class LabResults(Base):
    __tablename__ = "lab_results"

    result_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    test_name = Column(String, nullable=False)
    result_data = Column(String, nullable=False)

class MedicalHistory(Base):
    __tablename__ = "medical_history"

    history_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    condition = Column(String, nullable=False)
    treatment = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Can be NULL if ongoing


class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    medication = Column(String, nullable=False)
    dosage = Column(String, nullable=False)

class Reminder(Base):
    __tablename__ = "reminders"

    reminder_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    reminder_text = Column(String, nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)



class PatientUploadedDocs(Base):
    __tablename__ = "patient_uploaded_docs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    document_data = Column(JSON, nullable=False)  # JSONB for unstructured data
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AITranscriptions(Base):
    __tablename__ = "ai_transcriptions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    transcription_data = Column(JSON, nullable=False)  # JSONB for AI-generated transcriptions
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DiagnosticInsights(Base):
    __tablename__ = "diagnostic_insights"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    insights = Column(JSON, nullable=False)  # JSONB for AI-generated insights
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EHRSummary(Base):
    __tablename__ = "ehr_summary"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    ehr_data = Column(JSON, nullable=False)  # JSONB for Electronic Health Records
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class FollowupRecommendations(Base):
    __tablename__ = "followup_recommendations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    recommendations = Column(JSON, nullable=False)  # JSONB for AI-generated follow-ups
    recommended_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class HealthMonitoringLogs(Base):
    __tablename__ = "health_monitoring_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    monitoring_data = Column(JSON, nullable=False)  # JSONB for health tracking data
    logged_at = Column(DateTime, default=datetime.utcnow, nullable=False)