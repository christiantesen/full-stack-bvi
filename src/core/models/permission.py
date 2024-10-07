from src.core.connection import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

class Permission(Base):
    
    __tablename__ = "permissions"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    name: str = Column(String(300), unique=True, nullable=False)
    description: str = Column(Text)
    
    module_id: int = mapped_column(ForeignKey("modules.id"))
    
    module = relationship("Module", foreign_keys=[module_id])