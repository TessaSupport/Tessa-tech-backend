from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from authentication.Oauth2 import create_access_token, get_current_user
from models.user import User
from utils.hash import Hash
from schemas.auth import LoginRequest
from schemas.user import UserPublic

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Create token with consistent data structure
    token_data = {
        "sub": user.username,
        "role": user.role,
        "parent_company": user.parent_company
    }
    token = create_access_token(data=token_data)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserPublic.model_validate(user)
    }

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    # Optional: store token in blacklist DB/Redis for true server-side logout
    return {"message": "Logged out successfully"}
