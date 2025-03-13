import os  
from dotenv import load_dotenv  
from datetime import datetime, timedelta  
from passlib.context import CryptContext  
from jose import jwt, JWTError  
from fastapi import Depends, HTTPException, status  
from fastapi.security import OAuth2PasswordBearer  

# Load environment variables  
load_dotenv()  

# Fetch the secret key from the environment variables  
SECRET_KEY = os.getenv("SECRET_KEY")  
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

# Initialize the password context for hashing  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  

# OAuth2 scheme to extract token from Authorization header  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:  
    return pwd_context.hash(password)  

def verify_password(plain_password: str, hashed_password: str) -> bool:  
    return pwd_context.verify(plain_password, hashed_password)  

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:  
    to_encode = data.copy()  
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))  
    to_encode.update({"exp": expire})  
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  

def get_current_user(token: str = Depends(oauth2_scheme)):  
    """
    Extract and validate JWT token to get current user details.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:  
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        email: str = payload.get("sub")  
        role: str = payload.get("role")  

        if email is None or role is None:  
            raise credentials_exception  

        return {"email": email, "role": role}  

    except JWTError:  
        raise credentials_exception  
    


