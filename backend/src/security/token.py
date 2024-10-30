from base64 import b85encode, b85decode
from jose import jwt
from sqlalchemy.orm import Session
from datetime import timedelta
from src.core.settings import get_settings
from fastapi import HTTPException, status
from src import utils, core

class TokenManager:
    """
    Clase para gestionar la creación, verificación y eliminación de tokens JWT.
    """
    
    TYPES_TOKEN = ["access", "refresh"]
    
    def __init__(self):
        self.settings = get_settings()
        self.cache_tokens = []
        self.logger_config = utils.LoggerConfig()
        self.hyre = self.logger_config.get_logger()
        self.token_model = core.models.Token
        self.dt_util = utils.DateTimeUtils()

    def str_encode(self, string: str) -> str:
        """Codifica una cadena en Base85."""
        return b85encode(string.encode('ascii')).decode('ascii')

    def str_decode(self, string: str) -> str:
        """Decodifica una cadena de Base85."""
        return b85decode(string.encode('ascii')).decode('ascii')

    def create_token(self, payload: dict, secret: str, algo: str) -> str:
        """Crea un token JWT a partir de un payload."""
        return jwt.encode(payload, secret, algorithm=algo)

    def token_payload(self, token: str, secret: str, algo: str):
        """Decodifica un token JWT y devuelve el payload."""
        try:
            return jwt.decode(token, secret, algorithms=algo)
        except Exception as jwt_exec:
            self.hyre.error(f"JWT Error: {str(jwt_exec)}")
            return None

    def generate_token(self, user_id: int, db: Session):
        """
        Genera un token para el usuario.

        Args:
            user_id (int): ID del usuario.
            db (Session): Conexión a la base de datos.

        Returns:
            Tuple[str, str, int]: Access token, refresh token y tiempo de expiración.
        
        Raises:
            HTTPException: En caso de error.
        """
        current_time = self.dt_util.default_datetime()
        
        user_token = next((token for token in self.cache_tokens if token.user_id == user_id), None)
        exists_token = True
        
        if user_token is None:
            user_token = db.query(self.token_model).filter(self.token_model.user_id == user_id).first()
            exists_token = False
        
        if user_token:
            if user_token.expires_at > current_time:
                if not exists_token:
                    self.cache_tokens.append(user_token)
                return self.degenerate_token(user_token.access_token, db, True)
            self.hyre.warning("Token expired for user with id: {id}").format(id=user_id)
            db.delete(user_token)
            db.commit()

        # Payload del access_token
        at_payload = {
            "sub": self.str_encode(user_id),
            "cre_at": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exp": int((current_time + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
            "type": self.str_encode(self.TYPES_TOKEN[0])
        }
        
        access_token = self.create_token(at_payload, self.settings.JWT_SECRET, self.settings.JWT_ALGORITHM)

        # Payload del refresh_token
        rt_expires = timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire_time = current_time + rt_expires
        
        rt_payload = {
            'sub': self.str_encode(user_id),
            'exp': int(expire_time.timestamp()),
            'type': self.str_encode(self.TYPES_TOKEN[1])
        }
        
        refresh_token = self.create_token(rt_payload, self.settings.SECRET_KEY, self.settings.JWT_ALGORITHM)
        
        new_token = self.token_model(
            user_id=user_id,
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
            db.rollback()
            self.hyre.error("Error generating token for user {id}: {e}").format(id=user_id, e=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "msg": self.logger_config.MSG_INTERNAL_SERVER_ERROR,
                    "errors": ["Error al generar el token."]
                }
            )
        
        self.hyre.success("Access token generated for user {id}").format(id=user_id)
        return access_token, refresh_token, rt_expires.seconds

    def degenerate_token(self, access_token: str, db: Session, exists: bool = False):
        """
        Elimina un token de la base de datos.

        Args:
            access_token (str): Token a eliminar.
            db (Session): Conexión a la base de datos.
            exists (bool): Indica si el token válido ya existe en la base de datos.

        Returns:
            Tuple[str, str, int] o int: Access token, refresh token y tiempo de expiración o ID del usuario.
        
        Raises:
            HTTPException: En caso de token no válido o expirado.
        """
        payload = self.token_payload(access_token, self.settings.JWT_SECRET, self.settings.JWT_ALGORITHM)

        if not payload:
            self.hyre.error("Invalid token provided")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "msg": "🔴 Vuelve a iniciar sesión.",
                    "errors": ["El token proporcionado no es válido."]
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        token_type = self.str_decode(payload.get("type"))
        if token_type != self.TYPES_TOKEN[0]:
            self.hyre.error("Invalid token type")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "msg": "🔴 Vuelve a iniciar sesión.",
                    "errors": ["El token proporcionado no corresponde a un token de acceso."]
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_id = int(self.str_decode(payload.get("sub")))
        data_token = next((token for token in self.cache_tokens if token.user_id == user_id and token.access_token == access_token), None)

        if data_token is None:
            data_token = db.query(self.token_model).filter(
                self.token_model.user_id == user_id,
                self.token_model.access_token == access_token
            ).first()
            if data_token is not None:
                self.cache_tokens.append(data_token)

        if not data_token:
            self.hyre.error("Token not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Vuelve a iniciar sesión.",
                    "errors": ["El token proporcionado no existe."]
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        current_time = self.dt_util.default_datetime()
        expires_in_seconds = int((data_token.expires_at - current_time).seconds)

        if expires_in_seconds <= 0:
            self.hyre.warning("Token expired for user {id}").format(id=user_id)
            db.delete(data_token)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "msg": "🔴 Vuelve a iniciar sesión.",
                    "errors": ["El token proporcionado ha expirado."]
                },
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        self.hyre.success("Token deaccess generated for user {id}").format(id=user_id)
        return access_token, data_token.refresh_token, expires_in_seconds if exists else user_id