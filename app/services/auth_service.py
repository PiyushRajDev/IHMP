from sqlalchemy.orm import Session
from app.models.model import User
from app.schemas.users import UserCreate
from app.core.security import hash_password, verify_password, create_access_token
from datetime import timedelta

def register_user(db: Session, user_data: UserCreate):
    hashed_pwd = hash_password(user_data.password)
    db_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_pwd, role=user_data.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def generate_token(user: User):
    return create_access_token({"sub": user.email, "role": user.role})
