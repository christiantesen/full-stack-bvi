from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship, mapped_column
from src.core.connection import Base

class Career(Base):
    __tablename__ = "careers"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    code: str = Column(String(10), index=True, unique=True)
    
    name: str = Column(String(150), index=True, unique=True)
    description: str = Column(Text)
    
    url_image: str = Column(Text, nullable=True)
    url_video: str = Column(Text, nullable=True)
    url_web: str = Column(Text, nullable=True)
    
    is_active: bool = Column(Boolean, default=True)