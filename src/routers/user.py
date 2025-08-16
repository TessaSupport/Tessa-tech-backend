from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user import UserCreate, UserResponse, OTPVerifyRequest
from db.db_user import create_DBuser
from authentication.Oauth2 import get_current_user
from models.user import User
from db.db_email import verify_user_email

router = APIRouter(
    prefix="/users",    
    tags=["users"]
)

@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    return create_DBuser(db, request)

@router.get('/me', response_model=UserResponse)
def get_my_user(user: User = Depends(get_current_user)):
    return user

@router.post("/verify-email")
def verify_email(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    return verify_user_email(db, request.email, request.otp)