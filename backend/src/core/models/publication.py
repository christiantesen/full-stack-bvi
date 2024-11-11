from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.core.connection import Base

from . import dt_utils

class Publication(Base):
    __tablename__ = "publications"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    title: str = Column(String(150), index=True, unique=True)
    description: str = Column(Text)
    
    image_path: str = Column(String(300), nullable=True)
    file_path: str = Column(String(300), nullable=True)
    
    average_rating = Column(Integer, default=0)  # Se puede actualizar cuando un rating es agregado o modificado
    
    is_active: bool = Column(Boolean, default=True)
    is_blocked: bool = Column(Boolean, default=False)
    
    uploaded_by: str = Column(Text, nullable=True)
    recommended_by: str = Column(Text, nullable=True)
    
    created_at: datetime = Column(DateTime, default=dt_utils.default_datetime())
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=dt_utils.default_datetime())
    
    career_id: Mapped[int] = mapped_column(ForeignKey('careers.id')) # Career ID
    career = relationship("Career", foreign_keys=[career_id])