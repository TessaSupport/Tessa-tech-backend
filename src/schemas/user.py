from pydantic import BaseModel, EmailStr
from typing import List, Optional
from .ticket import TicketInUser

class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number: str = None
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_verified: bool
    tickets: List[TicketInUser] = []
    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: Optional[str] = None
    is_verified: bool
    parent_company: Optional[str] = None
    role: str
    class Config:
        from_attributes = True

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str