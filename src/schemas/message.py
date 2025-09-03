from pydantic import BaseModel
from datetime import datetime
from schemas.status import SenderType

class MessageCreate(BaseModel):
    ticket_id: int
    sender_type: SenderType
    content: str

class MessageResponse(BaseModel):
    id: int
    ticket_id: int
    sender_type: SenderType
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
