from pydantic import model_validator, HttpUrl, ValidationError
from typing import Any, Optional
from fastapi import HTTPException, status

from . import base_model_config
from . import MsgResponse as msg_response
from . import char_validator

class Career(base_model_config.BaseRequest):
    code: str
    name: str
    description: str
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
        url_image = self.url_image.strip() if self.url_image else None
        url_video = self.url_video.strip() if self.url_video else None
        url_web = self.url_web.strip() if self.url_web else None
        
        # Validación de URLs usando HttpUrl
        def validate_url(url: str, field_name: str) -> None:
            try:
                HttpUrl(url)  # Valida creando una instancia de HttpUrl
            except ValidationError:
                errors.append(f"La URL del {field_name} no tiene un formato válido.")
        
        if url_image:
            if len(url_image) > 500:
                errors.append("La URL de la imagen no debe exceder los 500 caracteres.")
            url_image = url_image.strip()
            validate_url(url_image, "imagen")
        
        if url_video:
            if len(url_video) > 500:
                errors.append("La URL del video no debe exceder los 500 caracteres.")
            url_video = url_video.strip()
            validate_url(url_video, "video")
        
        if url_web:
            if len(url_web) > 500:
                errors.append("La URL de la página web no debe exceder los 500 caracteres.")
            url_web = url_web.strip()
            validate_url(url_web, "web")
            
        
        # Validar longitud del código
        if len(code) < 1 or len(code) > 10:
            errors.append("El código debe tener entre 1 y 10 caracteres.")
            
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
        if description and len(description) < 3:
            errors.append("La descripción debe tener al menos 3 caracteres.")
        if description and len(description) > 500:
            errors.append("La descripción no debe exceder los 500 caracteres.")
        if not description:
            errors.append("La descripción es obligatoria.")
                
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