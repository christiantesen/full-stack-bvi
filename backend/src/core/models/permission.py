from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship, mapped_column

from . import db_manager
from . import dt_utils

class Permission(db_manager.Base):
    
    __tablename__ = "permissions"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    name: str = Column(String(150), unique=True, nullable=False)
    description: str = Column(Text)
    
    created_at: datetime = Column(DateTime, default=dt_utils.default_datetime())
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=dt_utils.default_datetime())
    
    module_id: int = mapped_column(ForeignKey("modules.id"))
    
    module = relationship("Module", foreign_keys=[module_id])