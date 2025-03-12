from pydantic import BaseModel
from datetime import date, datetime
from app.models.model import RoleEnum, StatusEnum
from datetime import datetime
from typing import Dict, Any


class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str
    role: RoleEnum


class EHRSchema(BaseModel):
    patient_id: int
    diagnosis: str
    treatment: str
    notes: str


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime


class AppointmentResponse(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: StatusEnum


class AllergyTrackingCreate(BaseModel):
    user_id: int
    allergy_name: str
    reaction: str


class AllergyTrackingResponse(BaseModel):
    allergy_id: int
    user_id: int
    allergy_name: str
    reaction: str



class LabResultSchema(BaseModel):
    user_id: int
    test_name: str
    result_data: str


class MedicalHistorySchema(BaseModel):
    user_id: int
    condition: str
    treatment: str
    start_date: date
    end_date: date


class PrescriptionSchema(BaseModel):
    patient_id: int
    doctor_id: int
    medication: str
    dosage: str


class ReminderSchema(BaseModel):
    user_id: int
    reminder_text: str
    reminder_time: datetime

class PatientUploadedDocsSchema(BaseModel):
    user_id: int
    document_data: Dict[str, Any]  # JSONB field
    uploaded_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


# ✅ Schema for AI Transcriptions
class AITranscriptionsSchema(BaseModel):
    user_id: int
    transcription_data: Dict[str, Any]  # JSONB field
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


# ✅ Schema for Diagnostic Insights
class DiagnosticInsightsSchema(BaseModel):
    user_id: int
    insights: Dict[str, Any]  # JSONB field
    generated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


# ✅ Schema for EHR Summary
class EHRSummarySchema(BaseModel):
    user_id: int
    ehr_data: Dict[str, Any]  # JSONB field
    updated_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


# ✅ Schema for Follow-up Recommendations
class FollowupRecommendationsSchema(BaseModel):
    user_id: int
    recommendations: Dict[str, Any]  # JSONB field
    recommended_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


# ✅ Schema for Health Monitoring Logs
class HealthMonitoringLogsSchema(BaseModel):
    user_id: int
    monitoring_data: Dict[str, Any]  # JSONB field
    logged_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True


    class Config:
        orm_mode = True
