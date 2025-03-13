from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.database.database import engine, Base
from app.config import settings

# Initialize the FastAPI app
app = FastAPI(
    title="Your App Name",
    description="API for managing healthcare data",
    version="1.0.0",
)

# Include the API routers
app.include_router(api_router)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=Settings().debug)