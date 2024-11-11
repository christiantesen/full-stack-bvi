from fastapi import APIRouter, Depends, status
from typing import List
from src.api.schemas.user import MsgUserResponse, UserResponse, CreateUser, UpdateUser
from sqlalchemy.orm import Session
from src.api.controllers.user import get_all, get_by_id, create, update
from src.core.connection import DatabaseManager

db_manager = DatabaseManager()

rtr_user = APIRouter(
    prefix="/user",
    tags=["Users ✅"]
)

@rtr_user.post("/user", response_model=MsgUserResponse, status_code=status.HTTP_201_CREATED, name="User - Create 🆗")
async def c(user: CreateUser, db: Session = Depends(db_manager.get_db)):
    """
    Se crea un nuevo usuario.
    """
    data = create(db, user)
    data = UserResponse(
                id=data.id,
                username=data.username,
                full_name=data.full_name,
                paternal_name=data.paternal_name,
                maternal_name=data.maternal_name,
                email=data.email,
                phone=data.phone,
                is_active=data.is_active,
                is_blocked=data.is_blocked,
                career_id=data.career_id,
                role_id=data.role_id
            )
    return MsgUserResponse(msg="✅ El Usuario se ha creado exitosamente.", data=data)

@rtr_user.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK, name="Users - Get All 🆗")
async def r_all(db: Session = Depends(db_manager.get_db)):
    """
    Se obtienen todos los usuarios del sistema.
    """
    data = get_all(db)
    data = [
                UserResponse(
                    id=user.id,
                    username=user.username,
                    full_name=user.full_name,
                    paternal_name=user.paternal_name,
                    maternal_name=user.maternal_name,
                    email=user.email,
                    phone=user.phone,
                    is_active=user.is_active,
                    is_blocked=user.is_blocked,
                    career_id=user.career_id,
                    role_id=user.role_id
                )
                for user in data
            ]
    return data

@rtr_user.get("/user/{id}", response_model=MsgUserResponse, status_code=status.HTTP_200_OK, name="User - Get By ID 🆗")
async def r(id: int, db: Session = Depends(db_manager.get_db)):
    """
    Se obtiene un usuario por su ID.
    """
    data = get_by_id(db, id)
    data = UserResponse(
                id=data.id,
                username=data.username,
                full_name=data.full_name,
                paternal_name=data.paternal_name,
                maternal_name=data.maternal_name,
                email=data.email,
                phone=data.phone,
                is_active=data.is_active,
                is_blocked=data.is_blocked,
                career_id=data.career_id,
                role_id=data.role_id
            )
    return MsgUserResponse(msg="✅ Usuario encontrado.", data=data)

@rtr_user.put("/user/{id}", response_model=MsgUserResponse, status_code=status.HTTP_200_OK, name="User - Update 🆗")
async def u(id: int, user: UpdateUser, db: Session = Depends(db_manager.get_db)):
    """
    Se actualiza un usuario por su ID.
    """
    data = update(db, id, user)
    data = UserResponse(
                id=data.id,
                username=data.username,
                full_name=data.full_name,
                paternal_name=data.paternal_name,
                maternal_name=data.maternal_name,
                email=data.email,
                phone=data.phone,
                is_active=data.is_active,
                is_blocked=data.is_blocked,
                career_id=data.career_id,
                role_id=data.role_id
            )
    return MsgUserResponse(msg="✅ Usuario actualizado.", data=data)