from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.ticket import Ticket
from schemas.ticket import TicketCreate

def create_DBticket(db: Session, request: TicketCreate, user_id: int):
    try:
        new_ticket = Ticket(
            title=request.title,
            description=request.description,
            user_id=user_id
        )
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        return new_ticket
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ticket: {str(e)}"
        )
    
def get_DBtickets(db: Session):
    tickets = db.query(Ticket).all()
    if tickets == []:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="No tickets recorded")
    return tickets

def get_DBticket_id(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ticket with ID {ticket_id} not found")
    return ticket

def get_DBticket_by_status(db: Session, T_status: str):
    tickets = db.query(Ticket).filter(Ticket.status == T_status).all()
    if tickets == []:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f"No tickets with status {status} exist")
    return tickets

def get_DBticket_by_created_date(db: Session, created_date: str):
    tickets = db.query(Ticket).filter(Ticket.created_at == created_date).all()
    if tickets == []:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f"No tickets created on {created_date} exist")
    return tickets

def get_DBticket_by_priority(db: Session, priority: str):
    tickets = db.query(Ticket).filter(Ticket.priority == priority).all()
    if tickets == []:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=f"No tickets with priority {priority} exist")
    return tickets