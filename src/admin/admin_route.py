from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from schemas.user import UserCreate, UserResponse
from models.user import User
from typing import List
from db.db_user import get_DBusers, get_DBuser_by_username
from authentication.Oauth2 import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.get('/users/all', response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_DBusers(db)

@router.get('/users/{username}')
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return get_DBuser_by_username(db, username)

@router.get("/dashboard", dependencies=[Depends(lambda: get_current_user("admin"))])
def admin_dashboard():
    return {"message": "Welcome Admin!"}
