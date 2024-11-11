from fastapi import APIRouter, Depends, status
from typing import List
from src.api.schemas.user import MsgUserResponse, UserResponse, CreateUser, UpdateUser
from src.api.schemas.role import RoleResponse
from src.api.schemas.career import CareerResponse
from src.api.schemas.permission import PermissionResponse
from sqlalchemy.orm import Session
from src.api.controllers.user import get_all, get_by_id, create_1_2, create_3_4, update
from src.core.connection import DatabaseManager
from src.auth.current import current_user

db_manager = DatabaseManager()

rtr_user = APIRouter(
    prefix="/user",
    tags=["Users ✅"]
)

@rtr_user.post("/user/public", response_model=MsgUserResponse, status_code=status.HTTP_201_CREATED, name="User - Create 🆗")
async def c_1_2(user: CreateUser, db: Session = Depends(db_manager.get_db)):
    """
    Se crea un nuevo usuario. (Público/Alumno)
    """
    data = create_1_2(db, user)
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
                career=CareerResponse(
                    id=data.career.id,
                    code=data.career.code,
                    name=data.career.name,
                    description=data.career.description,
                    url_image=data.career.url_image,
                    url_video=data.career.url_video,
                    url_web=data.career.url_web,
                    is_active=data.career.is_active
                ) if data.career else None,
                role=RoleResponse(
                    id=data.role.id,
                    name=data.role.name,
                    description=data.role.description,
                    is_active=data.role.is_active,
                    created_at=data.role.created_at,
                    updated_at=data.role.updated_at,
                    permissions=[
                        PermissionResponse(
                            id=permission.id,
                            name=permission.name,
                            description=permission.description,
                            created_at=permission.created_at,
                            updated_at=permission.updated_at
                        )
                        for permission in data.role.permissions
                    ]
                )
            )
    return MsgUserResponse(msg="✅ El Usuario se ha creado exitosamente.", data=data)

@rtr_user.get("/user/public/me", response_model=MsgUserResponse, status_code=status.HTTP_201_CREATED, name="User[Profile] - Get Me 🆗")
async def p(db: Session = Depends(db_manager.get_db)):#, c_u: UserResponse = Depends(current_user)):
    pass#return MsgUserResponse(msg="✅ Perfil.", data=c_u)

@rtr_user.put("/user/public/{id}", response_model=MsgUserResponse, status_code=status.HTTP_200_OK, name="User - Update 🆗")
async def u_public(id: int, user: UpdateUser, db: Session = Depends(db_manager.get_db)):#, c_u: UserResponse = Depends(current_user)):
    """
    Se actualiza un usuario por su ID.
    """
    user.role_id = None
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
                career=CareerResponse(
                    id=data.career.id,
                    code=data.career.code,
                    name=data.career.name,
                    description=data.career.description,
                    url_image=data.career.url_image,
                    url_video=data.career.url_video,
                    url_web=data.career.url_web,
                    is_active=data.career.is_active
                ) if data.career else None,
                role=RoleResponse(
                    id=data.role.id,
                    name=data.role.name,
                    description=data.role.description,
                    is_active=data.role.is_active,
                    created_at=data.role.created_at,
                    updated_at=data.role.updated_at,
                    permissions=[
                        PermissionResponse(
                            id=permission.id,
                            name=permission.name,
                            description=permission.description,
                            created_at=permission.created_at,
                            updated_at=permission.updated_at
                        )
                        for permission in data.role.permissions
                    ]
                )
            )
    return MsgUserResponse(msg="✅ Usuario actualizado.", data=data)


@rtr_user.post("/user/private", response_model=MsgUserResponse, status_code=status.HTTP_201_CREATED, name="User - Create 🆗")
async def c_3_4(user: CreateUser, db: Session = Depends(db_manager.get_db)):#, c_u: UserResponse = Depends(current_user)):
    """
    Se crea un nuevo usuario. (Docente o Administrativo)
    """
    data = create_3_4(db, user)
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
                career=CareerResponse(
                    id=data.career.id,
                    code=data.career.code,
                    name=data.career.name,
                    description=data.career.description,
                    url_image=data.career.url_image,
                    url_video=data.career.url_video,
                    url_web=data.career.url_web,
                    is_active=data.career.is_active
                ) if data.career else None,
                role=RoleResponse(
                    id=data.role.id,
                    name=data.role.name,
                    description=data.role.description,
                    is_active=data.role.is_active,
                    created_at=data.role.created_at,
                    updated_at=data.role.updated_at,
                    permissions=[
                        PermissionResponse(
                            id=permission.id,
                            name=permission.name,
                            description=permission.description,
                            created_at=permission.created_at,
                            updated_at=permission.updated_at
                        )
                        for permission in data.role.permissions
                    ]
                )
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
                career=CareerResponse(
                    id=data.career.id,
                    code=data.career.code,
                    name=data.career.name,
                    description=data.career.description,
                    url_image=data.career.url_image,
                    url_video=data.career.url_video,
                    url_web=data.career.url_web,
                    is_active=data.career.is_active
                ) if data.career else None,
                role=RoleResponse(
                    id=data.role.id,
                    name=data.role.name,
                    description=data.role.description,
                    is_active=data.role.is_active,
                    created_at=data.role.created_at,
                    updated_at=data.role.updated_at,
                    permissions=[
                        PermissionResponse(
                            id=permission.id,
                            name=permission.name,
                            description=permission.description,
                            created_at=permission.created_at,
                            updated_at=permission.updated_at
                        )
                        for permission in data.role.permissions
                    ]
                )
            )
    return MsgUserResponse(msg="✅ Usuario encontrado.", data=data)

@rtr_user.put("/user/{id}/private", response_model=MsgUserResponse, status_code=status.HTTP_200_OK, name="User - Update 🆗")
async def u_private(id: int, user: UpdateUser, db: Session = Depends(db_manager.get_db)):
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
                career=CareerResponse(
                    id=data.career.id,
                    code=data.career.code,
                    name=data.career.name,
                    description=data.career.description,
                    url_image=data.career.url_image,
                    url_video=data.career.url_video,
                    url_web=data.career.url_web,
                    is_active=data.career.is_active
                ) if data.career else None,
                role=RoleResponse(
                    id=data.role.id,
                    name=data.role.name,
                    description=data.role.description,
                    is_active=data.role.is_active,
                    created_at=data.role.created_at,
                    updated_at=data.role.updated_at,
                    permissions=[
                        PermissionResponse(
                            id=permission.id,
                            name=permission.name,
                            description=permission.description,
                            created_at=permission.created_at,
                            updated_at=permission.updated_at
                        )
                        for permission in data.role.permissions
                    ]
                )
            )
    return MsgUserResponse(msg="✅ Usuario actualizado.", data=data)