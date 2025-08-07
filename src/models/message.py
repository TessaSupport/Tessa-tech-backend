from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy import Enum as sqlEnum, Column, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base
from .status import SenderType

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    sender_type = Column(sqlEnum(SenderType, name="sender_type_enum"), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="messages")
