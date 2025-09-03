from pydantic import BaseModel, Field
from datetime import datetime
from .status import TicketStatus

class TicketBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: str
    status: TicketStatus = TicketStatus.OPEN
    user_id: int

class TicketCreate(TicketBase):
    pass

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True

class TicketInUser(BaseModel):
    id: int
    title: str
    status: TicketStatus
    
    class Config:
        from_attributes = True