from src.core.models.user import User as user_model
from src.core.models.token import Token as token_model
from fastapi import HTTPException, status
from src.security.pwd import PasswordManager
from src.security.token import TokenManager
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR
from src.core.settings import get_settings
from datetime import datetime, timedelta

pm = PasswordManager()
tm = TokenManager()
settings = get_settings()

def auth_login(db, data):
    try:
        user = db.query(user_model).filter(user_model.username == data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Usuario no encontrado."]
                }
            )
    except HTTPException as e:
        hyre.error(f"{e.detail}")
        raise e
    except Exception as e:
        hyre.critical(f"{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": MSG_INTERNAL_SERVER_ERROR,
                "errors": []
            }
        )
    if not pm.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Error de Autenticación",
                    "errors": ["Contraseña incorrecta."]
                }
            )
    access_token, refresh_token, expires_in_seconds = tm.generate_token(db, user.id)
    return access_token, refresh_token, expires_in_seconds
    
def auth_refresh(db, refresh_token: str):
    try:
        refresh_token_payload = tm.token_payload(refresh_token,settings.JWT_SECRET,settings.JWT_ALGORITHM)
        if not refresh_token_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Error de Autenticación",
                    "errors": ["Token inválido."]
                }
            )
        if refresh_token_payload['type'] != tm.str_encode(tm.TYPES_TOKEN[1]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Error de Autenticación",
                    "errors": ["Token inválido."]
                }
            )
        token_db = db.query(token_model).filter(token_model.refresh_token == refresh_token).first()
        if not token_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Error de Autenticación",
                    "errors": ["Token inválido."]
                }
            )
        refresh_exp = datetime.fromtimestamp(refresh_token_payload['exp'])
        seconds_add_exp = timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_new_exp = refresh_exp + seconds_add_exp
        refresh_token_payload["exp"] = int(refresh_new_exp.timestamp())
        refresh_new_token = tm.generate_token(
            refresh_token_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)
        token_db.refresh_token = refresh_new_token
        token_db.expires_at = refresh_new_exp
        db.commit()
        db.refresh(token_db)
        return token_db.access_token, token_db.refresh_token, token_db.expires_at.seconds
    except HTTPException as e:
        hyre.error(f"{e.detail}")
        raise e
    except Exception as e:
        hyre.critical(f"{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": MSG_INTERNAL_SERVER_ERROR,
                "errors": []
            }
        )
        
def auth_logout(db, access_token: str):
    try:
        access_token_payload = tm.token_payload(access_token,settings.JWT_SECRET,settings.JWT_ALGORITHM)
        if not access_token_payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Error de Autenticación",
                    "errors": ["Token inválido."]
                }
            )
        if access_token_payload['type'] != tm.str_encode(tm.TYPES_TOKEN[0]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Error de Autenticación",
                    "errors": ["Token inválido."]
                }
            )
        token_db = db.query(token_model).filter(token_model.access_token == access_token).first()
        if not token_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Error de Autenticación",
                    "errors": ["Token inválido."]
                }
            )
        db.delete(token_db)
        db.commit()
        return True
    except HTTPException as e:
        hyre.error(f"{e.detail}")
        raise e
    except Exception as e:
        hyre.critical(f"{str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": MSG_INTERNAL_SERVER_ERROR,
                "errors": []
            }
        )