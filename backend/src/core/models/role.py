from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship, mapped_column

from . import db_manager
from . import dt_utils

class Role(db_manager.Base):
    
    __tablename__ = "roles"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    name: str = Column(String(50), unique=True, nullable=False)
    description: str = Column(Text)
    
    is_active: bool = Column(Boolean, default=True)
    
    created_at: datetime = Column(DateTime, default=dt_utils.default_datetime())
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=dt_utils.default_datetime())
    
    users = relationship("User", back_populates="role")