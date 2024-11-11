from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from datetime import datetime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.core.connection import Base

from . import dt_utils

class User(Base):
    __tablename__ = "users"
    
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    username: str = Column(String(15), unique=True, index=True)
    password: str = Column(Text)
    
    full_name: str = Column(String(50)) # Nombre completo
    paternal_name: str = Column(String(30)) # Apellido paterno
    maternal_name: str = Column(String(30)) # Apellido materno
    email: str = Column(String(255), unique=True, index=True)
    phone: str = Column(String(15), unique=True, index=True)
    sex: str = Column(String(1)) # M: Masculino, F: Femenino
    date_of_birth: datetime = Column(DateTime) # Fecha de nacimiento
    
    is_active: bool = Column(Boolean, default=True)
    is_blocked: bool = Column(Boolean, default=False)

    career_id: Mapped[int] = mapped_column(ForeignKey('careers.id')) # Career ID
    career = relationship("Career", foreign_keys=[career_id])
    
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id')) # 1: Publico, 2: Alumno, 3: Docente, 4: Administrativo
    role = relationship("Role", foreign_keys=[role_id])

    created_at: datetime = Column(DateTime, default=dt_utils.default_datetime())
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=dt_utils.default_datetime())