from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.auth_service import register_user, authenticate_user, generate_token
from app.schemas.users import UserCreate, UserLogin, Token

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    token = generate_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = generate_token(user)
    return {"access_token": token, "token_type": "bearer"}
