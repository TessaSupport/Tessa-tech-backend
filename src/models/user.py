from sqlalchemy.sql.sqltypes import String, Integer, DateTime, Boolean
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from db.baseClass import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="company_admin")  # or "sub_admin", "user"
    parent_company = Column(String, nullable=True)  # store company username if sub-admin/user
    created_at = Column(DateTime, default=func.now(), nullable=False)

    tickets = relationship("Ticket", back_populates="user")
    otps = relationship("OTP", back_populates="user", cascade="all, delete-orphan")
