from src.core.connection import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

class RoleModule(Base):
    
    __tablename__ = "role_modules"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    role_id: int = mapped_column(ForeignKey("roles.id"))
    module_id: int = mapped_column(ForeignKey("modules.id"))
    
    role = relationship("Role", foreign_keys=[role_id])
    module = relationship("Module", foreign_keys=[module_id])