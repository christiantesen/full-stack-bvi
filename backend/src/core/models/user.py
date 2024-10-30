from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship, mapped_column

from . import db_manager
from . import dt_utils

class User(db_manager.Base):
    __tablename__ = "users"
    
    id: str = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    username: str = Column(String(150), unique=True, index=True)
    password: str = Column(String(150))
    
    full_name: str = Column(String(300)) # Nombre completo
    paternal_name: str = Column(String(150)) # Apellido paterno
    maternal_name: str = Column(String(150)) # Apellido materno
    email: str = Column(String(150), unique=True, index=True)
    phone: str = Column(String(15), unique=True, index=True)
    
    is_active: bool = Column(Boolean, default=True)
    is_blocked: bool = Column(Boolean, default=False)

    career_id: int = mapped_column(ForeignKey('careers.id', nullable=True)) # Career ID
    career = relationship("Career", back_populates="users")
    
    role_id: int = mapped_column(ForeignKey('roles.id')) # 1: Publico, 2: Alumno, 3: Docente, 4: Administrativo
    role = relationship("Role", back_populates="users")

    created_at: datetime = Column(DateTime, default=dt_utils.default_datetime())
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=dt_utils.default_datetime())