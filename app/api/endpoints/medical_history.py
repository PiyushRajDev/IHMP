from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import MedicalHistory
from app.schemas import MedicalHistorySchema
from app.database.database import SessionLocal

router = APIRouter()

@router.post("/")
def add_medical_history(history: MedicalHistorySchema, db: Session = Depends(SessionLocal)):
    new_history = MedicalHistory(**history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return {"message": "Medical history added", "history_id": new_history.history_id}

@router.get("/{user_id}")
def get_medical_history(user_id: int, db: Session = Depends(SessionLocal)):
    history = db.query(MedicalHistory).filter(MedicalHistory.user_id == user_id).all()
    if not history:
        raise HTTPException(status_code=404, detail="No medical history found")
    return {"history": history}