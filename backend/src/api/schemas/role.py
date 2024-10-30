from pydantic import model_validator
from typing import Any, Optional
from fastapi import HTTPException, status
from datetime import datetime

from . import base_model_config
from . import msg_response
from . import char_validator

class Role(base_model_config.BaseRequest):
    name: str
    description: str

    @model_validator(mode="after")
    def validate_data(self) -> Any:
        errors = []

        # Accedemos directamente a los atributos del modelo
        name = self.name.strip()
        description = self.description.strip()

        # Validar longitud del nombre
        if len(name) < 3 or len(name) > 50:
            errors.append("El nombre debe tener entre 3 y 50 caracteres.")

        # Solo letras y espacios en el nombre
        if not all(char.isalpha() or char.isspace() for char in name):
            errors.append("El nombre solo puede contener letras.")

        # Filtrar caracteres no permitidos en la descripción si no está vacía
        if description:
            chars_not_permitted = [
                char for char in description if char in char_validator.FORBIDDEN_CHARS]
            chars_not_permitted = list(set(chars_not_permitted))
            if chars_not_permitted:
                errors.append("Los siguientes caracteres no están permitidos en la descripción: {x}".format(
                    x=', '.join(chars_not_permitted)))

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


class CreateRole(Role):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nombre del Rol",
                "description": "Descripción del Rol"
            }
        }


class UpdateRole(Role):
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Nombre del Rol",
                "description": "Descripción del Rol",
                "is_active": True
            }
        }


class RoleResponse(base_model_config.BaseResponse):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Nombre del Rol",
                "description": "Descripción del Rol",
                "is_active": True,
                "created_at": "2021-01-01T00:00:00",
                "updated_at": "2021-01-01T00:00:00"
            }
        }


class MsgRoleResponse(msg_response):
    data: RoleResponse

    class Config:
        json_schema_extra = {
            "example": {
                "msg": "Mensaje de respuesta",
                "data": {
                    "id": 1,
                    "name": "Nombre del Rol",
                    "description": "Descripción del Rol",
                    "is_active": True,
                    "created_at": "2021-01-01T00:00:00",
                    "updated_at": "2021-01-01T00:00:00"
                }
            }
        }
