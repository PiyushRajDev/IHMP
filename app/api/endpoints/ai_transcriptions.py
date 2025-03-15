from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.model import AITranscriptions
from app.schemas.scemas import AITranscriptionsSchema
from app.dependencies.database import get_db

router = APIRouter(
    prefix="/ai-transcriptions",
    tags=["ai transcriptions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def save_ai_transcription(transcription: AITranscriptionsSchema, db: Session = Depends(get_db)):
    new_transcription = AITranscriptions(**transcription.dict())
    db.add(new_transcription)
    db.commit()
    db.refresh(new_transcription)
    return {"message": "AI Transcription saved", "transcription_id": new_transcription.id}

@router.get("/{patient_id}")
def get_ai_transcriptions(patient_id: int, db: Session = Depends(get_db)):
    transcriptions = db.query(AITranscriptions).filter(AITranscriptions.user_id == patient_id).all()
    if not transcriptions:
        raise HTTPException(status_code=404, detail="No transcriptions found")
    return {"transcriptions": transcriptions}