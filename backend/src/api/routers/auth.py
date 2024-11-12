from fastapi import APIRouter, Depends, status
from src.api.schemas.auth import AuthResponse
from src.api.controllers.auth import auth_login, auth_refresh, auth_logout
from src.core.connection import DatabaseManager
from src.auth.current import current_user, UserResponse
from src.utils.login_form import OAuth2PasswordRequestForm2Params
from src.utils.out_msg import MsgResponse

db_manager = DatabaseManager()

rtr_auth = APIRouter(
    prefix="/auth",
    tags=["Auth ✅"]
)

@rtr_auth.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK, name="Auth - Login")
async def login(db = Depends(db_manager.get_db), data: OAuth2PasswordRequestForm2Params = Depends()):
    """
    Iniciar sesión
    """
    access_token, refresh_token, expires_in_seconds = auth_login(db, data)
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in_seconds=expires_in_seconds
    )
    
@rtr_auth.post("/refresh", response_model=AuthResponse, status_code=status.HTTP_200_OK, name="Auth - Refresh")
async def refresh(refresh_token: str, db = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Refrescar token
    """
    access_token, refresh_token, expires_in_seconds = auth_refresh(db, refresh_token)
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in_seconds=expires_in_seconds
    )
    
@rtr_auth.post("/logout", status_code=status.HTTP_200_OK, name="Auth - Logout", response_model=MsgResponse)
async def logout(db = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Cerrar sesión
    """
    auth_logout(db)
    return MsgResponse(msg="Sesión cerrada correctamente.")