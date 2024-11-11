from pydantic import model_validator
from typing import Any, Optional
from fastapi import HTTPException, status

from . import base_model_config
from . import MsgResponse as msg_response
from . import char_validator

class Career(base_model_config.BaseRequest):
    code: str
    name: str
    description: str = None
    url_image: Optional[str] = None
    url_video: Optional[str] = None
    url_web: Optional[str] = None
    
    @model_validator(mode="after")
    def validate_data(self) -> Any:
        errors = []
        
        # Accedemos directamente a los atributos del modelo
        code = self.code.strip()
        name = self.name.strip()
        description = self.description.strip()
        
        # Validar longitud del código
        if len(code) < 3 or len(code) > 50:
            errors.append("El código debe tener entre 3 y 50 caracteres.")
            
        # Filtrar caracteres no permitidos en el código
        chars_not_permitted = [
            char for char in name if char in char_validator.FORBIDDEN_CHARS]
        chars_not_permitted = list(set(chars_not_permitted))
        if chars_not_permitted:
            errors.append("Los siguientes caracteres no están permitidos en el código: {x}".format(
                x=', '.join(chars_not_permitted)))
            
        # Validar longitud del nombre
        if len(name) < 3 or len(name) > 150:
            errors.append("El nombre debe tener entre 3 y 150 caracteres.")
            
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
    
class CreateCareer(Career):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "code": "Código de la Carrera",
                "name": "Nombre de la Carrera",
                "description": "Descripción de la Carrera",
                "url_image": "URL de la imagen de la Carrera",
                "url_video": "URL del video de la Carrera",
                "url_web": "URL de la página web de la Carrera"
            }
        }
        
class UpdateCareer(Career):
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "code": "Código de la Carrera",
                "name": "Nombre de la Carrera",
                "description": "Descripción de la Carrera",
                "url_image": "URL de la imagen de la Carrera",
                "url_video": "URL del video de la Carrera",
                "url_web": "URL de la página web de la Carrera",
                "is_active": True
            }
        }
        
class CareerResponse(base_model_config.BaseResponse):
    id: int
    code: str
    name: str
    description: str
    url_image: Optional[str] = None
    url_video: Optional[str] = None
    url_web: Optional[str] = None
    is_active: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "code": "Código de la Carrera",
                "name": "Nombre de la Carrera",
                "description": "Descripción de la Carrera",
                "url_image": "URL de la imagen de la Carrera",
                "url_video": "URL del video de la Carrera",
                "url_web": "URL de la página web de la Carrera",
                "is_active": True
            }
        }
        
class MsgCareerResponse(msg_response):
    data: CareerResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "msg": "Mensaje de respuesta",
                "data": {
                    "id": 1,
                    "code": "Código de la Carrera",
                    "name": "Nombre de la Carrera",
                    "description": "Descripción de la Carrera",
                    "url_image": "URL de la imagen de la Carrera",
                    "url_video": "URL del video de la Carrera",
                    "url_web": "URL de la página web de la Carrera",
                    "is_active": True
                }
            }
        }