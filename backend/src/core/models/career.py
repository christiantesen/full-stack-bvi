from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship, mapped_column

from . import db_manager

class Career(db_manager.Base):

    __tablename__ = "careers"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    code: str = Column(String(50), index=True, unique=True)
    
    name: str = Column(String(150), index=True, unique=True)
    description: str = Column(Text)
    
    url_image: str = Column(String(300), nullable=True)
    url_video: str = Column(String(300), nullable=True)
    url_web: str = Column(String(300), nullable=True)
    
    is_active: bool = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="career")