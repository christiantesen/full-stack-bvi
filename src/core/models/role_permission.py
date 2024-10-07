from src.core.connection import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

class RolePermission(Base):
    
    __tablename__ = "role_permissions"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    role_id: int = mapped_column(ForeignKey("roles.id"))
    permission_id: int = mapped_column(ForeignKey("permissions.id"))
    
    role = relationship("Role", foreign_keys=[role_id])
    permission = relationship("Permission", foreign_keys=[permission_id])