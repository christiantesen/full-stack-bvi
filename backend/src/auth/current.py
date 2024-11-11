from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.security.token import TokenManager
from src.utils.logger import hyre
from src.api.controllers.user import get_by_id as get_user_by_id
from src.api.schemas.user import UserResponse
from src.api.schemas.role import RoleResponse
from src.api.schemas.career import CareerResponse
from src.api.schemas.permission import PermissionResponse
from src.core.connection import DatabaseManager

db_manager = DatabaseManager()
token_manager = TokenManager()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db_manager.get_db)) -> UserResponse:
    """
    Obtiene el usuario actual
    """
    # Comprobación de la validez del token
    user_id = token_manager.degenerate_token(token, db)
    
    # Datos del usuario
    user = get_user_by_id(db, user_id)
    errors = []
    
    # Verificar si el usuario a sido bloqueado
    if user.is_blocked:
        hyre.warning("User does not have access.")
        errors.append("El usuario fue bloqueado.")
    
    # Verificar si el usuario está activo
    if not user.is_active:
        hyre.warning("User is disabled.")
        errors.append("El usuario está deshabilitado.")
        
    # Verificar si el rol del usuario está activo
    if not user.role.is_active:
        hyre.warning("Role is disabled.") 
        errors.append("El rol de; usuario está deshabilitado.")

    # Lanzar excepciones si hay errores
    if errors:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "🔴 Error de Autorización",
                "errors": errors
            }
        )
    
    hyre.success("User {x} is active and has access.".format(x=user.username))
    return UserResponse(
                id=user.id,
                username=user.username,
                full_name=user.full_name,
                paternal_name=user.paternal_name,
                maternal_name=user.maternal_name,
                email=user.email,
                phone=user.phone,
                is_active=user.is_active,
                is_blocked=user.is_blocked,
                career=CareerResponse(
                    id=user.career.id,
                    code=user.career.code,
                    name=user.career.name,
                    description=user.career.description,
                    url_image=user.career.url_image,
                    url_video=user.career.url_video,
                    url_web=user.career.url_web,
                    is_active=user.career.is_active
                ) if user.career else None,
                role=RoleResponse(
                    id=user.role.id,
                    name=user.role.name,
                    description=user.role.description,
                    is_active=user.role.is_active,
                    created_at=user.role.created_at,
                    updated_at=user.role.updated_at,
                    permissions=[
                        PermissionResponse(
                            id=permission.id,
                            name=permission.name,
                            description=permission.description,
                            created_at=permission.created_at,
                            updated_at=permission.updated_at
                        )
                        for permission in user.role.permissions
                    ]
                )
            )