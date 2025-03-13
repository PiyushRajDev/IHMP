from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.model import PatientUploadedDocs
from app.schemas.scemas import PatientUploadedDocsSchema
from app.dependencies.database import get_db

router = APIRouter(
    prefix="/patient-documents",
    tags=["patient documents"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def upload_patient_document(doc_data: PatientUploadedDocsSchema, db: Session = Depends(get_db)):
    new_doc = PatientUploadedDocs(**doc_data.dict())
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {"message": "Patient document uploaded", "document_id": new_doc.id}

@router.get("/{patient_id}")
def get_patient_documents(patient_id: int, db: Session = Depends(get_db)):
    documents = db.query(PatientUploadedDocs).filter(PatientUploadedDocs.user_id == patient_id).all()
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    return {"documents": documents}