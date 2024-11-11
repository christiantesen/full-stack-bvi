from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.core.connection import Base

class RolePermission(Base):
    
    __tablename__ = "role_permissions"
    
    id: int = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role = relationship("Role", foreign_keys=[role_id])
    
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))
    permission = relationship("Permission", foreign_keys=[permission_id])