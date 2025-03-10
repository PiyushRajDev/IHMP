from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.database.database import engine, Base
from app.models.model import User, EHR, Appointment, AllergyTracking, LabResults, MedicalHistory, Prescription, Reminder
 # Ensure models are imported


# Initialize FastAPI App
app = FastAPI(title="IHMP API")

# Include Routers
app.include_router(api_router)

# Create Database

@app.get("/")
def root():
    return {"message": "IHMP API is Running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
