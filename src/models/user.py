from sqlalchemy.sql.sqltypes import String, Integer, DateTime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    tickets = relationship("Ticket", back_populates="user")