from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_ticket import (
    create_DBticket, get_DBtickets, 
    get_DBticket_id, 
    get_DBticket_by_status, 
    get_DBticket_by_created_date,
    get_DBticket_by_priority
)
from schemas.ticket import TicketCreate, TicketResponse

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)

@router.post("/create", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(request: TicketCreate, user_id: int, db: Session = Depends(get_db)):
    return create_DBticket(db, request, user_id)


@router.get("/all", response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    return get_DBtickets(db)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket_by_id(ticket_id: int, db: Session = Depends(get_db)):
    return get_DBticket_id(db, ticket_id)


@router.get("/status/{status}", response_model=list[TicketResponse])
def get_tickets_by_status(status: str, db: Session = Depends(get_db)):
    return get_DBticket_by_status(db, status)


@router.get("/created_at/{created_date}", response_model=list[TicketResponse])
def get_tickets_by_created_date(created_date: str, db: Session = Depends(get_db)):
    return get_DBticket_by_created_date(db, created_date)

@router.get("/priority/{priority}", response_model=list[TicketResponse])
def get_tickets_by_priority(priority: str, db: Session = Depends(get_db)):
    return get_DBticket_by_priority(db, priority)