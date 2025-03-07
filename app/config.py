import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Correct import
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Error: DATABASE_URL is not set in environment variables.")

# PostgreSQL Connection
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:  # Use a context manager to test connection
        print("Database connection established successfully!")  
except Exception as e:
    print(f"Error connecting to database: {e}")
    engine = None  # Set engine to None if the connection fails

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class for ORM models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
