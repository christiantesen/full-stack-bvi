from pydantic import model_validator, EmailStr, constr
from typing import Any, Optional
from fastapi import HTTPException, status

from . import base_model_config
from . import msg_response
from . import char_validator

class User(base_model_config.BaseRequest):
    username: str
    password: str
    full_name: str
    paternal_name: Optional[str] = None
    maternal_name: Optional[str] = None
    email: EmailStr
    phone: Optional[constr(pattern=r'^\+?[0-9\s-]{8,15}$')] = None  # type: ignore # Formato de teléfono internacional
    career_id: Optional[int] = None
    role_id: int

    @model_validator(mode="after")
    def validate_data(self) -> Any:
        errors = []
        
        # Validaciones para el username
        username = self.username.strip()
        if len(username) < 3 or len(username) > 150:
            errors.append("El nombre de usuario debe tener entre 3 y 150 caracteres.")
        chars_not_permitted = [char for char in username if char in char_validator.FORBIDDEN_CHARS]
        if chars_not_permitted:
            errors.append("Los siguientes caracteres no están permitidos en el nombre de usuario: {x}".format(
                x=', '.join(set(chars_not_permitted))))
        
        # Validaciones para el nombre completo
        full_name = self.full_name.strip()
        if len(full_name) < 3 or len(full_name) > 300:
            errors.append("El nombre completo debe tener entre 3 y 300 caracteres.")
        if not all(char.isalpha() or char.isspace() for char in full_name):
            errors.append("El nombre completo solo puede contener letras y espacios.")
        
        # Validaciones para el teléfono
        if self.phone and not self.phone.replace(' ', '').replace('-', '').isdigit():
            errors.append("El teléfono solo puede contener números, espacios y guiones.")

        # Lanzar excepciones si hay errores
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "🔴 Error de validación.",
                    "errors": errors
                }
            )
        
        return self

class CreateUser(User):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "username": "nombre_usuario",
                "password": "ContraseñaSegura123",
                "full_name": "Nombre Completo",
                "paternal_name": "Apellido Paterno",
                "maternal_name": "Apellido Materno",
                "email": "usuario@dominio.com",
                "phone": "+123456789",
                "career_id": 1,
                "role_id": 2
            }
        }

class UpdateUser(User):
    is_active: Optional[bool] = None
    is_blocked: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "nombre_usuario",
                "password": "NuevaContraseña123",
                "full_name": "Nombre Completo",
                "paternal_name": "Apellido Paterno",
                "maternal_name": "Apellido Materno",
                "email": "usuario@dominio.com",
                "phone": "+123456789",
                "is_active": False,
                "is_blocked": True,
                "career_id": 1,
                "role_id": 3
            }
        }

class UserResponse(base_model_config.BaseResponse):
    id: int
    username: str
    full_name: str
    paternal_name: Optional[str] = None
    maternal_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool
    is_blocked: bool
    career_id: Optional[int] = None
    role_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "nombre_usuario",
                "full_name": "Nombre Completo",
                "paternal_name": "Apellido Paterno",
                "maternal_name": "Apellido Materno",
                "email": "usuario@dominio.com",
                "phone": "+123456789",
                "is_active": True,
                "is_blocked": False,
                "career_id": 1,
                "role_id": 2
            }
        }

class MsgUserResponse(msg_response):
    data: UserResponse

    class Config:
        json_schema_extra = {
            "example": {
                "msg": "Usuario registrado correctamente",
                "data": {
                    "id": 1,
                    "username": "nombre_usuario",
                    "full_name": "Nombre Completo",
                    "paternal_name": "Apellido Paterno",
                    "maternal_name": "Apellido Materno",
                    "email": "usuario@dominio.com",
                    "phone": "+123456789",
                    "is_active": True,
                    "is_blocked": False,
                    "career_id": 1,
                    "role_id": 2
                }
            }
        }
