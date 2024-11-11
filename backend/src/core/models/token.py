from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from src.core.connection import Base

from . import dt_utils

class Token(Base):
    __tablename__ = "tokens"
    
    id: int = Column(Integer, primary_key=True, index=True,
                     unique=True, autoincrement=True)
    access_token: str = Column(
        String(255), nullable=True, index=True, default=None)
    refresh_token: str = Column(
        String(255), nullable=True, index=True, default=None)
    created_at: datetime = Column(DateTime, default=dt_utils.default_datetime())
    expires_at: datetime = Column(DateTime)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", foreign_keys=[user_id])