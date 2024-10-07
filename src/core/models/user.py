from src.core.connection import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from src.utils.time_server import default_datetime

class User(Base):
    __tablename__ = "users"
    
    id: str = Column(String(15), primary_key=True, index=True, unique=True)
    
    full_name: str = Column(String(300)) # Nombre completo
    paternal_surname: str = Column(String(150)) # Apellido paterno
    maternal_surname: str = Column(String(150)) # Apellido materno
    email: str = Column(String(150), unique=True, index=True)
    phone: str = Column(String(15), unique=True, index=True)
    password: str = Column(String(150))
    
    career: int = Column(Integer) # Carrera
    
    is_active: bool = Column(Boolean, default=True)
    role_id: int = Column(Integer) # 1: Publico, 2: Alumno, 3: Docente, 4: Administrativo
    
    created_at: datetime = Column(DateTime, default=default_datetime)
    updated_at: datetime = Column(DateTime, nullable=True,
                        default=None, onupdate=default_datetime)