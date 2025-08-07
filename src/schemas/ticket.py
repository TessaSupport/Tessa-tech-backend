from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

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
    status: TicketStatus
    created_at: datetime
    class Config:
        from_attributes = True

class TicketInUser(BaseModel):
    title: str
    status: TicketStatus
    class Config:
        from_attributes = True