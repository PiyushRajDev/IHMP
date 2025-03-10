from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.model import AITranscriptions, DiagnosticInsights, EHRSummary, FollowupRecommendations, HealthMonitoringLogs, PatientUploadedDocs, User, EHR, Appointment, AllergyTracking,LabResults,MedicalHistory,Prescription,Reminder
from app.schemas.scemas import AITranscriptionsSchema, DiagnosticInsightsSchema, EHRSummarySchema, FollowupRecommendationsSchema, HealthMonitoringLogsSchema, PatientUploadedDocsSchema, UserSchema, EHRSchema, AppointmentCreate, AllergyTrackingCreate,LabResultSchema,MedicalHistorySchema,PrescriptionSchema,ReminderSchema
from app.database.database import SessionLocal
from app.models.model import LabResults
from app.schemas.scemas import LabResultSchema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User added", "user": user}


@router.post("/ehr/")
def create_ehr(ehr: EHRSchema, db: Session = Depends(get_db)):
    new_ehr = EHR(**ehr.dict())
    db.add(new_ehr)
    db.commit()
    db.refresh(new_ehr)
    return {"message": "EHR added", "record_id": new_ehr.record_id}


@router.get("/ehr/{patient_id}")
def get_ehrs(patient_id: int, db: Session = Depends(get_db)):
    records = db.query(EHR).filter(EHR.patient_id == patient_id).all()
    if not records:
        raise HTTPException(status_code=404, detail="No EHR found")
    return {"records": records}


@router.post("/appointments/")
def create_appointment(appointment_data: AppointmentCreate, db: Session = Depends(get_db)):
    patient = db.query(User).filter(User.user_id == appointment_data.patient_id, User.role == "Patient").first()
    doctor = db.query(User).filter(User.user_id == appointment_data.doctor_id, User.role == "Doctor").first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointment = Appointment(
        patient_id=patient.user_id,
        doctor_id=doctor.user_id,
        appointment_date=appointment_data.appointment_date,
        status="Scheduled"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment created", "appointment_id": appointment.appointment_id}


@router.get("/appointments/{doctor_id}")
def get_appointments(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(User).filter(User.user_id == doctor_id, User.role == "Doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    appointments = db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    if not appointments:
        return {"message": "No appointments found for this doctor"}

    return {"doctor_id": doctor_id, "appointments": appointments}


@router.post("/allergies/")
def create_allergy(allergy_data: AllergyTrackingCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == allergy_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    allergy = AllergyTracking(**allergy_data.dict())
    db.add(allergy)
    db.commit()
    db.refresh(allergy)
    return {"message": "Allergy added", "allergy_id": allergy.allergy_id}

@router.get("/allergies/{user_id}")
def get_allergies(user_id: int, db: Session = Depends(get_db)):
   
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

 
    allergies = db.query(AllergyTracking).filter(AllergyTracking.user_id == user_id).all()

    if not allergies:
        raise HTTPException(status_code=404, detail="No allergies found for this user")

    return {"user_id": user_id, "allergies": allergies}


@router.post("/lab-results/")
def add_lab_result(lab_result: LabResultSchema, db: Session = Depends(get_db)):
    new_result = LabResults(**lab_result.dict())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return {"message": "Lab result added", "result_id": new_result.result_id}


@router.get("/lab-results/{user_id}")
def get_lab_results(user_id: int, db: Session = Depends(get_db)):
    results = db.query(LabResults).filter(LabResults.user_id == user_id).all()
    if not results:
        raise HTTPException(status_code=404, detail="No lab results found")
    return {"results": results}


@router.post("/medical-history/")
def add_medical_history(history: MedicalHistorySchema, db: Session = Depends(get_db)):
    new_history = MedicalHistory(**history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return {"message": "Medical history added", "history_id": new_history.history_id}


@router.get("/medical-history/{user_id}")
def get_medical_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(MedicalHistory).filter(MedicalHistory.user_id == user_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No medical history found")
    return {"history": history}



@router.post("/prescriptions/")
def add_prescription(prescription: PrescriptionSchema, db: Session = Depends(get_db)):
    # Check if patient exists
    patient = db.query(User).filter(User.user_id == prescription.patient_id, User.role == "Patient").first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

   
    doctor = db.query(User).filter(User.user_id == prescription.doctor_id, User.role == "Doctor").first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_prescription = Prescription(**prescription.dict())
    db.add(new_prescription)
    db.commit()
    db.refresh(new_prescription)
    return {"message": "Prescription added", "prescription_id": new_prescription.prescription_id}


@router.get("/prescriptions/{patient_id}")
def get_prescriptions(patient_id: int, db: Session = Depends(get_db)):
    prescriptions = db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
    if not prescriptions:
        raise HTTPException(status_code=404, detail="No prescriptions found")
    return {"prescriptions": prescriptions}

@router.post("/reminders/")
def add_reminder(reminder: ReminderSchema, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.user_id == reminder.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_reminder = Reminder(
        user_id=reminder.user_id,
        reminder_text=reminder.reminder_text,
        reminder_time=reminder.reminder_time
    )
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)
    return {"message": "Reminder added", "reminder_id": new_reminder.reminder_id}


@router.get("/reminders/{user_id}")
def get_reminders(user_id: int, db: Session = Depends(get_db)):
    reminders = db.query(Reminder).filter(Reminder.user_id == user_id).all()
    if not reminders:
        raise HTTPException(status_code=404, detail="No reminders found")
    return {"reminders": reminders}


# ✅ Upload Patient Document
@router.post("/patient-documents/")
def upload_patient_document(doc_data: PatientUploadedDocsSchema, db: Session = Depends(get_db)):
    new_doc = PatientUploadedDocs(**doc_data.dict())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {"message": "Patient document uploaded", "document_id": new_doc.id}


# ✅ Fetch Patient Documents
@router.get("/patient-documents/{patient_id}")
def get_patient_documents(patient_id: int, db: Session = Depends(get_db)):
    documents = db.query(PatientUploadedDocs).filter(PatientUploadedDocs.user_id == patient_id).all()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    return {"documents": documents}


# ✅ Store AI Transcription
@router.post("/ai-transcriptions/")
def save_ai_transcription(transcription: AITranscriptionsSchema, db: Session = Depends(get_db)):
    new_transcription = AITranscriptions(**transcription.dict())
    db.add(new_transcription)
    db.commit()
    db.refresh(new_transcription)
    return {"message": "AI Transcription saved", "transcription_id": new_transcription.id}


# ✅ Retrieve AI Transcriptions
@router.get("/ai-transcriptions/{patient_id}")
def get_ai_transcriptions(patient_id: int, db: Session = Depends(get_db)):
    transcriptions = db.query(AITranscriptions).filter(AITranscriptions.user_id == patient_id).all()
    if not transcriptions:
        raise HTTPException(status_code=404, detail="No transcriptions found")
    return {"transcriptions": transcriptions}


# ✅ Store Diagnostic Insights
@router.post("/diagnostic-insights/")
def add_diagnostic_insights(insights: DiagnosticInsightsSchema, db: Session = Depends(get_db)):
    new_insight = DiagnosticInsights(**insights.dict())
    db.add(new_insight)
    db.commit()
    db.refresh(new_insight)
    return {"message": "Diagnostic insights stored", "insight_id": new_insight.id}


# ✅ Fetch Diagnostic Insights
@router.get("/diagnostic-insights/{patient_id}")
def get_diagnostic_insights(patient_id: int, db: Session = Depends(get_db)):
    insights = db.query(DiagnosticInsights).filter(DiagnosticInsights.user_id == patient_id).all()
    if not insights:
        raise HTTPException(status_code=404, detail="No diagnostic insights found")
    return {"insights": insights}


# ✅ Store EHR Summary
@router.post("/ehr-summaries/")
def store_ehr_summary(summary: EHRSummarySchema, db: Session = Depends(get_db)):
    new_summary = EHRSummary(**summary.dict())
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    return {"message": "EHR Summary saved", "summary_id": new_summary.id}


# ✅ Fetch EHR Summary
@router.get("/ehr-summaries/{patient_id}")
def get_ehr_summaries(patient_id: int, db: Session = Depends(get_db)):
    summaries = db.query(EHRSummary).filter(EHRSummary.user_id == patient_id).all()
    if not summaries:
        raise HTTPException(status_code=404, detail="No EHR summaries found")
    return {"ehr_summaries": summaries}


# ✅ Store Follow-up Recommendations
@router.post("/followup-recommendations/")
def add_followup_recommendation(recommendation: FollowupRecommendationsSchema, db: Session = Depends(get_db)):
    new_recommendation = FollowupRecommendations(**recommendation.dict())
    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)
    return {"message": "Follow-up recommendation added", "recommendation_id": new_recommendation.id}


# ✅ Fetch Follow-up Recommendations
@router.get("/followup-recommendations/{patient_id}")
def get_followup_recommendations(patient_id: int, db: Session = Depends(get_db)):
    recommendations = db.query(FollowupRecommendations).filter(FollowupRecommendations.user_id == patient_id).all()
    if not recommendations:
        raise HTTPException(status_code=404, detail="No follow-up recommendations found")
    return {"recommendations": recommendations}


# ✅ Store Health Monitoring Logs (IoT & Wearable Data)
@router.post("/health-monitoring-logs/")
def store_health_log(log: HealthMonitoringLogsSchema, db: Session = Depends(get_db)):
    new_log = HealthMonitoringLogs(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"message": "Health monitoring log saved", "log_id": new_log.id}


# ✅ Fetch Health Monitoring Logs
@router.get("/health-monitoring-logs/{patient_id}")
def get_health_monitoring_logs(patient_id: int, db: Session = Depends(get_db)):
    logs = db.query(HealthMonitoringLogs).filter(HealthMonitoringLogs.user_id == patient_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No health logs found")
    return {"health_logs": logs}