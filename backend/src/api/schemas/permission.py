from src.utils.base import BaseRequest, BaseResponse
from pydantic import model_validator
from typing import Any, Optional
from fastapi import HTTPException, status
from src.utils.characteres import FORBIDDEN_CHARS
from datetime import datetime
from src.utils.out_msg import MsgResponse

class Permission(BaseRequest):
    name: str
    description: Optional[str] = None
    
    @model_validator(mode="after")
    def validate_data(self) -> Any:
        errors = []
        
        # Accedemos directamente a los atributos del modelo
        name = self.name.strip()
        description = self.description.strip()
        
        # Validar longitud del nombre
        if len(name) < 3 or len(name) > 150:
            errors.append("El nombre debe tener entre 3 y 150 caracteres.")
            
        # Filtrar caracteres no permitidos en el nombre
        chars_not_permitted = [
            char for char in name if char in FORBIDDEN_CHARS]
        chars_not_permitted = list(set(chars_not_permitted))
        if chars_not_permitted:
            errors.append("Los siguientes caracteres no están permitidos en el nombre: {x}".format(
                x=', '.join(chars_not_permitted)))
            
        # Filtrar caracteres no permitidos en la descripción si no está vacía
        if description:
            chars_not_permitted = [
                char for char in description if char in FORBIDDEN_CHARS]
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
    
class CreatePermission(Permission):
    module_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Permiso 1",
                "description": "Descripción del permiso 1",
                "module_id": 1
            }
        }
        
class UpdatePermission(Permission):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Permiso 1",
                "description": "Descripción del permiso 1"
            }
        }
        
class PermissionResponse(BaseResponse):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    module_id: int

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Permiso 1",
                "description": "Descripción del permiso 1",
                "created_at": "2021-08-01T00:00:00",
                "updated_at": "2021-08-01T00:00:00",
                "module_id": 1
            }
        }
        
class MsgPermissionResponse(MsgResponse):
    data: PermissionResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "msg": "Mensaje de respuesta",
                "data": {
                    "id": 1,
                    "name": "Permiso 1",
                    "description": "Descripción del permiso 1",
                    "created_at": "2021-08-01T00:00:00",
                    "updated_at": "2021-08-01T00:00:00",
                    "module_id": 1
                }
            }
        }