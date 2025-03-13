from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    PATIENT = "Patient"
    DOCTOR = "Doctor"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
