# crud/user.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.otps import OTP
from utils.email import send_email
from utils.otp import verify_otp  # Use the utility function

def verify_user_email(db: Session, email: str, otp: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Use the utility function instead of duplicating logic
    success, message = verify_otp(user, otp, db)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    # Send welcome email
    send_email(
        to=user.email,
        subject="Welcome to Our Service!",
        body=f"Hello {user.username}, your account is now verified. Welcome!"
    )

    return {"message": "Email verified successfully"}
