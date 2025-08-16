from sqlalchemy.orm.session import Session
from models.user import User
from schemas.user import UserCreate
from fastapi import HTTPException, status
from utils.hash import Hash
from utils.otp import create_and_send_otp

def create_DBuser(db: Session, request: UserCreate):
    # Check for duplicate username
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists"
        )
    
    # Check for duplicate email
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already exists"
        )
    
    # Check for duplicate phone number if provided
    if request.phone_number:
        existing_phone = db.query(User).filter(User.phone_number == request.phone_number).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Phone number already exists"
            )
    
    try:
        new_user = User(
            username=request.username,
            email=request.email,
            phone_number=request.phone_number,
            password=Hash.bcrypt(request.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Send OTP for email verification
        create_and_send_otp(new_user, db)
        
        return new_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

def get_DBusers(db: Session):
    users = db.query(User).all()
    if users == []:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='No users found')
    return users

def get_DBuser_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")
    return user