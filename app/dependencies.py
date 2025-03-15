from sqlalchemy.orm import Session
from app.database.database import SessionLocal

# Dependency to get a database session
def get_db():
    db: Session = SessionLocal()  # Create a new session
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Close the session after request is completed
