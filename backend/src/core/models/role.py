from src.core.connection import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
from src.utils.time_server import default_datetime

class Role(Base):
    
    __tablename__ = "roles"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    name: str = Column(String(50), unique=True, nullable=False)
    description: str = Column(Text)
    
    is_active: bool = Column(Boolean, default=True)
    
    created_at: datetime = Column(DateTime, default=default_datetime)
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=default_datetime)