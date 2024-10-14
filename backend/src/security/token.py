from base64 import b85encode, b85decode
from jose import jwt
from sqlalchemy.orm import Session
from src.core.models.token import Token as token_model
from src.utils.time_server import default_datetime
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR
from datetime import timedelta
from src.core.settings import get_settings
from fastapi import HTTPException, status

settings = get_settings()

def str_encode(str: str) -> str:  # ? Validado
    return b85encode(str.encode('ascii')).decode('ascii')

def str_decode(str: str) -> str:  # ? Validado
    return b85decode(str.encode('ascii')).decode('ascii')

def create_token(payload: dict, secret: str, algo: str):
    return jwt.encode(payload, secret, algorithm=algo)

def token_payload(token: str, secr, algo):  # ? Validado
    try:
        payload = jwt.decode(token, secr, algorithms=algo)
    except Exception as jwt_exec:
        print(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload

CACHE_TOKENS = []
TYPES_TOKEN = ["access", "refresh"]

def generate_token(id, db: Session):
    """
    Generación de un token para el usuario
    
    args:
        id: int -> id del usuario
        db: Session -> conexión a la base de datos
        
    returns:
        access_token: str -> token de acceso
        refresh_token: str -> token de refresco
        rt_expires: int -> tiempo de expiración del token
        
    raises:
        HTTPException -> en caso de error
    """
    
    current_time = default_datetime()
    
    user_token = next((token for token in CACHE_TOKENS if token.user_id == id), None)
    exit_token = True
    if user_token is None:
        user_token = db.query(token_model).filter(token_model.user_id == id).first()
        exit_token = False
    
    # Si el token ya existe y no ha expirado, se retorna
    if user_token:
        if user_token.expires_at > current_time:
            if not exit_token:
                CACHE_TOKENS.append(user_token)
            return degenerate_token(user_token.access_token, db)
        hyre.warning("Token expired for user with id: {id}").format(id=id)
        db.delete(user_token)
        db.commit()
    
    # Payload del access_token, ahora incluye el campo de expiración
    at_payload = {
        "sub": str_encode(id),
        "cre_at": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "exp": int((current_time + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),  # Expiración
        "type": str_encode(TYPES_TOKEN[0])
    }
    
    access_token = create_token(
        at_payload,
        settings.JWT_SECRET,
        settings.JWT_ALGORITHM
    )
    
    rt_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_time = current_time + rt_expires
    
    # Payload del refresh_token
    rt_payload = {
        'sub': str_encode(id),
        'exp': int(expire_time.timestamp()),
        'type': str_encode(TYPES_TOKEN[1])
    }
    refresh_token = create_token(
        rt_payload,
        settings.SECRET_KEY,
        settings.JWT_ALGORITHM
    )
    
    new_token = token_model(
        user_id=id,
        access_token=access_token,
        refresh_token=refresh_token,
        created_at=current_time,
        expires_at=expire_time
    )
    try:
        if user_token is not None:
            db.delete(user_token)
        db.add(new_token)
        db.commit()
    except Exception as e:
        db.rollback()  # Revertimos cambios en caso de error
        hyre.error("Error generating token for user {id}: {e}").format(id=id, e=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": MSG_INTERNAL_SERVER_ERROR,
                "errors": [
                    "Error al generar el token."
                ]
            }
        )
    
    # No loggear el token directamente por razones de seguridad
    hyre.success("Access token generated for user {id}").format(id=id)
    
    return access_token, refresh_token, rt_expires.seconds

def degenerate_token(access_token: str, db: Session):
    """
    Elimina un token de la base de datos
    
    args:
        token: str -> token a eliminar
        db: Session -> conexión a la base de datos
    """
    
    # Decodificamos el payload del token
    payload = token_payload(
        access_token,
        settings.JWT_SECRET,
        settings.JWT_ALGORITHM
        )
    
    # Si el payload no es válido, retornamos
    if not payload:
        hyre.error("Invalid token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "Vuelve a iniciar sesión.",
                "errors": [
                    "El token proporcionado no es válido."
                ]
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    type = str_decode(payload.get("type"))
    if type != TYPES_TOKEN[0]:
        hyre.error("Invalid token type")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "Vuelve a iniciar sesión.",
                "errors": [
                    "El token proporcionado no corresponde a un token de acceso."
                ]
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Decodificamos el id del usuario
    user_id = int(str_decode(payload.get("sub")))
    
    # Buscamos el token en el cache
    data_token = next((token for token in CACHE_TOKENS if token.user_id == user_id and token.access_token == access_token), None)
    exit_token = True
    if data_token is None:
        data_token = db.query(token_model).filter(
            token_model.user_id == user_id,
            token_model.access_token == access_token
        ).first()
        exit_token = False
        
    # Si el token no existe, retornamos
    if not data_token:
        hyre.error("Token not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "Vuelve a iniciar sesión.",
                "errors": [
                    "El token proporcionado no existe."
                ]
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    current_time = default_datetime()
        
    # Calculamos el tiempo de expiración
    expires_in_seconds = int((data_token.expires_at - current_time).seconds)
    
    # Si el token ha expirado, retornamos
    if expires_in_seconds <= 0:
        hyre.warning("Token expired for user {id}").format(id=user_id)
        db.delete(data_token)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "msg": "Vuelve a iniciar sesión.",
                "errors": [
                    "El token proporcionado ha expirado."
                ]
            },
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    hyre.success("Token deaccess generated for user {id}").format(id=user_id)
    
    return access_token, data_token.refresh_token, expires_in_seconds