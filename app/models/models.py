from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.config import Base


class User(Base):  
    __tablename__ = "users"  

    user_id = Column(Integer, primary_key=True, index=True)  
    username = Column(String, nullable=False)  
    email = Column(String, unique=True, nullable=False)  
    password = Column(String, nullable=False)  
    role = Column(String)  
    phone_number = Column(String)  

    ehrs = relationship("EHR", back_populates="user", cascade="all, delete-orphan")  # Relationship to EHR


class EHR(Base):  
    __tablename__ = "ehr"  

    record_id = Column(Integer, primary_key=True, index=True)  
    patient_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))  
    diagnosis = Column(Text, nullable=False)  
    treatment = Column(Text, nullable=False)  
    notes = Column(Text)  

    user = relationship("User", back_populates="ehrs")  # Correct placement of relationship

