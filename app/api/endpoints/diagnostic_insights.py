from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.model import DiagnosticInsights
from app.schemas.scemas import DiagnosticInsightsSchema
from app.dependencies.database import get_db

router = APIRouter(
    prefix="/diagnostic-insights",
    tags=["diagnostic insights"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def add_diagnostic_insights(insights: DiagnosticInsightsSchema, db: Session = Depends(get_db)):
    new_insight = DiagnosticInsights(**insights.dict())
    db.add(new_insight)
    db.commit()
    db.refresh(new_insight)
    return {"message": "Diagnostic insights stored", "insight_id": new_insight.id}

@router.get("/{patient_id}")
def get_diagnostic_insights(patient_id: int, db: Session = Depends(get_db)):
    insights = db.query(DiagnosticInsights).filter(DiagnosticInsights.user_id == patient_id).all()
    if not insights:
        raise HTTPException(status_code=404, detail="No diagnostic insights found")
    return {"insights": insights}