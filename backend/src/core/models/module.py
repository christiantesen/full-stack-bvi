from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from src.core.connection import Base

from . import dt_utils

class Module(Base):
    
    __tablename__ = "modules"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    name: str = Column(String(50), unique=True, nullable=False)
    description: str = Column(Text)
    
    is_active: bool = Column(Boolean, default=True)
    
    created_at: datetime = Column(DateTime, default=dt_utils.default_datetime())
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=dt_utils.default_datetime())