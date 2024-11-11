from pydantic import model_validator, EmailStr, constr
from typing import Any, Optional
from fastapi import HTTPException, status
from datetime import datetime

from . import base_model_config
from . import MsgResponse as msg_response
from . import char_validator

from src.api.schemas.role import RoleResponse
from src.api.schemas.career import CareerResponse


class User(base_model_config.BaseRequest):
    password: str
    full_name: str
    paternal_name: str
    maternal_name: str
    email: EmailStr
    phone: Optional[constr(pattern=r'^\+?[0-9\s-]{8,15}$')] = None # type: ignore # Formato de teléfono internacional
    sex: str
    date_of_birth: datetime
    career_id: Optional[int] = None
    role_id: int

    @model_validator(mode="after")
    def validate_data(self) -> Any:
        errors = []

        # Validaciones para el username
        username = self.username.strip()
        if len(username) < 3 or len(username) > 15:
            errors.append(
                "El nombre de usuario debe tener entre 3 y 15 caracteres.")
        chars_not_permitted = [
            char for char in username if char in char_validator.FORBIDDEN_CHARS]
        if chars_not_permitted:
            errors.append("Los siguientes caracteres no están permitidos en el nombre de usuario: {x}".format(
                x=', '.join(set(chars_not_permitted))))

        # Validaciones para la contraseña
        password = self.password.strip()
        if len(password) < 3 or len(password) > 15:
            errors.append("La contraseña debe tener entre 3 y 15 caracteres.")

        # Validaciones para el nombre completo
        full_name = self.full_name.strip()
        if len(full_name) < 3 or len(full_name) > 50:
            errors.append(
                "El nombre completo debe tener entre 3 y 50 caracteres.")
        if not all(char.isalpha() or char.isspace() for char in full_name):
            errors.append(
                "El nombre completo solo puede contener letras y espacios.")

        # Validaciones para el apellido paterno
        paternal_name = self.paternal_name.strip()
        if len(paternal_name) < 3 or len(paternal_name) > 30:
            errors.append(
                "El apellido paterno debe tener entre 3 y 30 caracteres.")
        if not all(char.isalpha() or char.isspace() for char in paternal_name):
            errors.append(
                "El apellido paterno solo puede contener letras y espacios.")

        # Validaciones para el apellido materno
        maternal_name = self.maternal_name.strip()
        if len(maternal_name) < 3 or len(maternal_name) > 30:
            errors.append(
                "El apellido materno debe tener entre 3 y 30 caracteres.")
        if not all(char.isalpha() or char.isspace() for char in maternal_name):
            errors.append(
                "El apellido materno solo puede contener letras y espacios.")

        # Validaciones para el teléfono
        if self.phone and not self.phone.replace(' ', '').replace('-', '').replace('+', '').isdigit():
            errors.append(
                "El teléfono solo puede contener números, espacios, guiones y el signo +.")

        # Validaciones para el sexo
        if self.sex not in ['M', 'F']:
            errors.append("El sexo solo puede ser 'M' o 'F'.")

        # Validaciones para la fecha de nacimiento
        if self.date_of_birth > datetime.now():
            errors.append(
                "La fecha de nacimiento no puede ser mayor a la fecha actual.")

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
    username: str
    
    @model_validator(mode="after")
    def validate_data(self) -> Any:
        errors = []

        # Validaciones para el username
        username = self.username.strip()
        if len(username) < 3 or len(username) > 15:
            errors.append(
                "El nombre de usuario debe tener entre 3 y 15 caracteres.")
        chars_not_permitted = [
            char for char in username if char in char_validator.FORBIDDEN_CHARS]
        if chars_not_permitted:
            errors.append("Los siguientes caracteres no están permitidos en el nombre de usuario: {x}".format(
                x=', '.join(set(chars_not_permitted))))

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
                "sex": "M",
                "date_of_birth": "2000-01-01",
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
                "password": "NuevaContraseña123",
                "full_name": "Nombre Completo",
                "paternal_name": "Apellido Paterno",
                "maternal_name": "Apellido Materno",
                "email": "usuario@dominio.com",
                "phone": "+123456789",
                "sex": "M",
                "date_of_birth": "2000-01-01",
                "is_active": False,
                "is_blocked": True,
                "career_id": 1,
                "role_id": 2
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
    career: Optional[CareerResponse] = None
    role: RoleResponse

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
                "sex": "M",
                "date_of_birth": "2000-01-01",
                "is_active": True,
                "is_blocked": False,
                "career": {
                    "id": 1,
                    "code": "Código de la Carrera",
                    "name": "Nombre de la Carrera",
                    "description": "Descripción de la Carrera",
                    "url_image": "URL de la imagen de la Carrera",
                    "url_video": "URL del video de la Carrera",
                    "url_web": "URL de la página web de la Carrera",
                    "is_active": True
                },
                "role": {
                    "id": 1,
                    "name": "Nombre del Rol",
                    "description": "Descripción del Rol",
                    "is_active": True,
                    "created_at": "2021-01-01T00:00:00",
                    "updated_at": "2021-01-01T00:00:00",
                    "permissions": [
                        {
                            "id": 1,
                            "name": "Permiso 1",
                            "description": "Descripción del permiso 1",
                            "created_at": "2022-01-01T00:00:00",
                            "updated_at": "2022-01-01T00:00:00"
                        }
                    ]
                }
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
                    "sex": "M",
                    "date_of_birth": "2000-01-01",
                    "is_active": True,
                    "is_blocked": False,
                    "career": {
                        "id": 1,
                        "code": "Código de la Carrera",
                        "name": "Nombre de la Carrera",
                        "description": "Descripción de la Carrera",
                        "url_image": "URL de la imagen de la Carrera",
                        "url_video": "URL del video de la Carrera",
                        "url_web": "URL de la página web de la Carrera",
                        "is_active": True
                    },
                    "role": {
                        "id": 1,
                        "name": "Nombre del Rol",
                        "description": "Descripción del Rol",
                        "is_active": True,
                        "created_at": "2021-01-01T00:00:00",
                        "updated_at": "2021-01-01T00:00:00",
                        "permissions": [
                            {
                                "id": 1,
                                "name": "Permiso 1",
                                "description": "Descripción del permiso 1",
                                "created_at": "2022-01-01T00:00:00",
                                "updated_at": "2022-01-01T00:00:00"
                            }
                        ]
                    }
                }
            }
        }