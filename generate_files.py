# generate_files.py
import os

# Define the base directory where your files will be generated
BASE_DIR = "app"

# Define your model and schema names
modules = [
    "user", "doctor", "patient", "appointment", "ehr", "prescription",
    "lab_report", "feedback", "recovery", "reminder", "pharmacy"
]

# Define template for SQLAlchemy models
model_template = '''from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.database import Base

class {ClassName}(Base):
    __tablename__ = '{tablename}'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
'''

# Define template for Pydantic schemas
schema_template = '''from pydantic import BaseModel
from typing import Optional

class {ClassName}Base(BaseModel):
    name: str
    description: Optional[str] = None
'''

# Ensure the folders exist
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "schemas"), exist_ok=True)

# Create model and schema files
for module in modules:
    model_name = module.capitalize()
    tablename = module + "s"
    
    # Write model file
    with open(f"{BASE_DIR}/models/{module}.py", "w") as f:
        f.write(model_template.format(ClassName=model_name, tablename=tablename))
        
    # Write schema file
    with open(f"{BASE_DIR}/schemas/{module}.py", "w") as f:
        f.write(schema_template.format(ClassName=model_name))

print("✅ All models and schemas generated successfully!")
