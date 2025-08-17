from sqlalchemy.sql.sqltypes import String, Integer, DateTime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from db.baseClass import Base
from datetime import datetime

class OTP(Base):
    __tablename__ = "email_otps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    otp_hash = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="otps")