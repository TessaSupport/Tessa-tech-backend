from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models.user import User
from db.database import get_db
from sqlalchemy.orm.session import Session
from authentication import Oauth2
from utils.hash import Hash

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/token")
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect credentials")

    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect credentials")
    
    token_data = {
        "sub": user.username,
        "role": user.role,
        "parent_company": user.parent_company
    }
    access_token = Oauth2.create_access_token(token_data)

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "parent_company": user.parent_company   
        }
    }