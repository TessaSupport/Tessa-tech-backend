from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.user import UserCreate, UserResponse
from db.db_user import create_DBuser

router = APIRouter(
    prefix="/users",    
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    return create_DBuser(db, request)