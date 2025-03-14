from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import FollowupRecommendations
from app.schemas import FollowupRecommendationsSchema
from app.database.database import SessionLocal

router = APIRouter()

@router.post("/")
def add_followup_recommendation(recommendation: FollowupRecommendationsSchema, db: Session = Depends(SessionLocal)):
    new_recommendation = FollowupRecommendations(**recommendation.dict())
    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)
    return {"message": "Follow-up recommendation added", "recommendation_id": new_recommendation.id}

@router.get("/{patient_id}")
def get_followup_recommendations(patient_id: int, db: Session = Depends(SessionLocal)):
    recommendations = db.query(FollowupRecommendations).filter(FollowupRecommendations.user_id == patient_id).all()
    if not recommendations:
        raise HTTPException(status_code=404, detail="No follow-up recommendations found")
    return {"recommendations": recommendations}