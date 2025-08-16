from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy import Column
from db.baseClass import Base
from datetime import datetime

class PendingUser(Base):
    __tablename__ = "pending_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    otp = Column(String, nullable=False)
    otp_expiry = Column(DateTime, nullable=False)
    role = Column(String, default="company_admin")
    created_at = Column(DateTime, default=datetime.utcnow)
