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