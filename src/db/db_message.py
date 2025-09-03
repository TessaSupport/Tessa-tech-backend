from sqlalchemy.orm import Session
from models.message import Message
from schemas.message import MessageCreate
from fastapi import HTTPException, status

def create_DBmessage(db: Session, request: MessageCreate):
    new_message = Message(
        ticket_id=request.ticket_id,
        sender_type=request.sender_type,
        content=request.content
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_DBmessages_by_ticket(db: Session, ticket_id: int):
    messages = db.query(Message).filter(Message.ticket_id == ticket_id).all()
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No messages found for ticket ID {ticket_id}"
        )
    return messages