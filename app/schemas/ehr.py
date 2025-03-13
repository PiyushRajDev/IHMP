from pydantic import BaseModel

class EHRSchema(BaseModel):
    patient_id: int
    diagnosis: str
    treatment: str
    notes: str

    class Config:
        orm_mode = True