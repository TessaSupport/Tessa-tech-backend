from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in the environment variables")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
if not ALGORITHM:
    raise ValueError("ALGORITHM must be set in the environment variables")

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
if not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be set in the environment variables")
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt