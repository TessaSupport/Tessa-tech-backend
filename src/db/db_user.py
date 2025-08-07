from sqlalchemy.orm.session import Session
from models.user import User
from schemas.user import UserCreate, UserResponse
from fastapi import HTTPException, status
from utils.hash import Hash

def create_DBuser(db: Session, request: UserCreate):
    new_user = User(
        username=request.username,
        email=request.email,
        phone_number=request.phone_number,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user