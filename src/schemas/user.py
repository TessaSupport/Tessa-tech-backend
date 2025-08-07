from pydantic import BaseModel, EmailStr
from typing import List
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
    tickets: List[TicketInUser] = []
    class Config:
        from_attributes = True