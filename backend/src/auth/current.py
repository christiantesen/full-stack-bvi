from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.security.token import degenerate_token
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def current_user(db: Session, token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual
    """
    # Comprobación de la validez del token
    user_id = degenerate_token(token, db)
    
    # Datos del usuario
    user = {} # Cambiar por la función que obtiene los datos del usuario
    errors = []
    
    # Verificar si el usuario a sido bloqueado
    if not user.allows_access:
        hyre.warning("User does not have access.")
        errors.append("El usuario no tiene acceso.")
    
    # Verificar si el usuario está activo
    if not user.is_active:
        hyre.warning("User is disabled.")
        errors.append("El usuario está deshabilitado.")
        
    # Verificar si el rol del usuario está activo
    if not user.role.is_active:
        hyre.warning("Role is disabled.")
        errors.append("El tipo de usuario está deshabilitado.")

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
    return user