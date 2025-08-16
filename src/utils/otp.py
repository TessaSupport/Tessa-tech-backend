import random
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User
from models.otps import OTP
from utils.email import send_otp_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_otp():
    return str(random.randint(100000, 999999))

def create_and_send_otp(user: User, db: Session):
    otp_value = generate_otp()
    otp_hash = pwd_context.hash(otp_value)
    otp_entry = OTP(
        user_id=user.id,
        otp_hash=otp_hash,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    db.add(otp_entry)
    db.commit()
    
    # Try to send email, but don't fail if it doesn't work
    try:
        send_otp_email(
            to=user.email,
            username=user.username,
            otp=otp_value
        )
        print(f"[INFO] OTP {otp_value} generated for user {user.username}")
    except Exception as e:
        print(f"[WARNING] Email failed but OTP generated: {otp_value}")
        print(f"[WARNING] User can still verify with this OTP")

def verify_otp(user: User, otp: str, db: Session):
    otp_record = (
        db.query(OTP)
        .filter(OTP.user_id == user.id)
        .order_by(OTP.created_at.desc())
        .first()
    )
    if not otp_record:
        return False, "No OTP found."

    if datetime.utcnow() > otp_record.expires_at:
        return False, "OTP expired."

    if not pwd_context.verify(otp, otp_record.otp_hash):
        return False, "Invalid OTP."

    # OTP is valid — verify user
    user.is_verified = True
    db.delete(otp_record)
    db.commit()
    return True, "Email verified successfully."
