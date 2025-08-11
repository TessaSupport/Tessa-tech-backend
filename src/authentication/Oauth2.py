from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from utils.config import settings
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user
from models.user import User
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = db_user.get_DBuser_by_username(db, username)
  if user is None:
    raise credentials_exception
  user.token_claims = payload
  return user


def require_admin(user: User = Depends(get_current_user)):
    """
    Ensures the current user is an admin.
    Checks either `is_admin` claim OR `scope` claim in JWT.
    """
    claims = getattr(user, "token_claims", {})

    # Option 1: is_admin boolean
    if claims.get("is_admin", False) is True:
        return user

    # Option 2: scope contains 'admin'
    scopes: List[str] = claims.get("scope", "").split()
    if "admin" in scopes:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
    )