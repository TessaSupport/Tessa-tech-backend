from sqlalchemy.sql.sqltypes import String, Integer, DateTime, Text
from sqlalchemy import Column, ForeignKey, Enum as sqlEnum
from sqlalchemy.orm import relationship
from db.baseClass import Base
from sqlalchemy.sql import func
from schemas.status import TicketStatus, TicketPriority, SenderType

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(sqlEnum(TicketStatus, name='status_enum'), default=TicketStatus.OPEN, nullable=False)
    priority = Column(sqlEnum(TicketPriority, name="priority_enum"), default=TicketPriority.MEDIUM, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    assigned_to = Column(sqlEnum(SenderType, name='sender_enum'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="tickets")
    messages = relationship("Message", back_populates="ticket", cascade="all, delete-orphan")
