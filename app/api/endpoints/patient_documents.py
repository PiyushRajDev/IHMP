from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import PatientUploadedDocs
from app.schemas import PatientUploadedDocsSchema
from app.dependencies import get_db

router = APIRouter()

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