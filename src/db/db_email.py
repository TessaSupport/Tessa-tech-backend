# crud/user.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.otps import OTP
from utils.email import email_service
from utils.otp import verify_otp
from typing import Dict, Any

def verify_user_email(db: Session, email: str, otp: str) -> Dict[str, Any]:
    """
    Verify user email using OTP and send welcome email
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    success, message = verify_otp(user, otp, db)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=message
        )

    # Send welcome email with correct parameters
    email_service.send_welcome_email(
        to=user.email,
        username=user.username
    )

    return {"message": "Email verified successfully"}
