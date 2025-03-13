from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.model import User

router = APIRouter()

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}! You have access to this protected route."}

