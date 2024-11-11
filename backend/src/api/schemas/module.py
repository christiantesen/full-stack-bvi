from pydantic import model_validator
from typing import Any, Optional, List
from fastapi import HTTPException, status
from datetime import datetime

from .permission import PermissionResponse
from . import base_model_config
from . import MsgResponse as msg_response
from . import char_validator


class Module(base_model_config.BaseRequest):
    name: str
    description: Optional[str] = None

    @model_validator(mode="after")
    def validate_data(self) -> Any:
        errors = []

        # Accedemos directamente a los atributos del modelo
        name = self.name.strip()
        description = self.description.strip()

        # Validar longitud del nombre
        if len(name) < 3 or len(name) > 50:
            errors.append("El nombre debe tener entre 3 y 50 caracteres.")

        # Filtrar caracteres no permitidos en el nombre
        chars_not_permitted = [
            char for char in name if char in char_validator.FORBIDDEN_CHARS]
        chars_not_permitted = list(set(chars_not_permitted))
        if chars_not_permitted:
            errors.append("Los siguientes caracteres no están permitidos en el nombre: {x}".format(
                x=', '.join(chars_not_permitted)))

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


class CreateModule(Module):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Módulo 1",
                "description": "Descripción del módulo 1"
            }
        }


class UpdateModule(Module):
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Módulo 1",
                "description": "Descripción del módulo 1",
                "is_active": True
            }
        }


class ModuleResponse(base_model_config.BaseResponse):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    permissions: Optional[List[PermissionResponse]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Módulo 1",
                "description": "Descripción del módulo 1",
                "is_active": True,
                "created_at": "2022-01-01T00:00:00",
                "updated_at": "2022-01-01T00:00:00",
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


class MsgModuleResponse(msg_response):
    data: ModuleResponse

    class Config:
        json_schema_extra = {
            "example": {
                "msg": "Módulo creado con éxito.",
                "data": {
                    "id": 1,
                    "name": "Módulo 1",
                    "description": "Descripción del módulo 1",
                    "is_active": True,
                    "created_at": "2022-01-01T00:00:00",
                    "updated_at": "2022-01-01T00:00:00",
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
