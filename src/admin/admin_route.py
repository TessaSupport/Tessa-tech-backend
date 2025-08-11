from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.database import get_db
from schemas.user import UserCreate, UserResponse
from models.user import User
from typing import List
from db.db_user import get_DBusers, get_DBuser_by_username
from authentication.Oauth2 import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)

@router.get('/users/all', response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_DBusers(db)

@router.get('/users/{username}')
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return get_DBuser_by_username(db, username)