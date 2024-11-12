from fastapi import APIRouter, Depends, status
from typing import List
from src.api.schemas.role import MsgRoleResponse, RoleResponse, CreateRole, UpdateRole, PermissionResponse
from sqlalchemy.orm import Session
from src.api.controllers.role import get_all, get_by_id, create, update, add_role_permission, remove_role_permission
from src.core.connection import DatabaseManager
from src.auth.current import current_user, UserResponse

db_manager = DatabaseManager()

rtr_role = APIRouter(
    prefix="/role",
    tags=["Roles[Permissions] ✅"]
)

#! ROLES
@rtr_role.post("/role", response_model=MsgRoleResponse, status_code=status.HTTP_201_CREATED, name="Role - Create 🆗")
async def c(role: CreateRole, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se crea un nuevo rol.
    """
    data = create(db, role)
    data = RoleResponse(
        id=data.id,
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        created_at=data.created_at,
        updated_at=data.updated_at,
        permissions=[
            PermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in data.permissions
        ]
    )
    return MsgRoleResponse(
        msg="✅ El Rol se ha creado exitosamente.",
        data=data)


@rtr_role.get("/roles", response_model=List[RoleResponse], status_code=status.HTTP_200_OK, name="Roles - Get All 🆗")
async def r_all(db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se obtienen todos los roles del sistema.
    """
    data = get_all(db)
    data = [RoleResponse(
        id=role.id,
        name=role.name,
        description=role.description,
        is_active=role.is_active,
        created_at=role.created_at,
        updated_at=role.updated_at,
        permissions=[
            PermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in role.permissions
        ]
    )
        for role in data
    ]
    return data


@rtr_role.get("/role/{id}", response_model=MsgRoleResponse, status_code=status.HTTP_200_OK, name="Role - Get By ID 🆗")
async def r(id: int, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se obtiene un rol por su ID.
    """
    data = get_by_id(db, id)
    data = RoleResponse(
        id=data.id,
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        created_at=data.created_at,
        updated_at=data.updated_at,
        permissions=[
            PermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in data.permissions
        ]
    )
    return MsgRoleResponse(msg="✅ Rol encontrado exitosamente.", data=data)


@rtr_role.put("/role/{id}", response_model=MsgRoleResponse, status_code=status.HTTP_200_OK, name="Role - Update 🆗")
async def u(id: int, role: UpdateRole, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se actualiza un rol por su ID.
    """
    data = update(db, id, role)
    data = RoleResponse(
        id=data.id,
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        created_at=data.created_at,
        updated_at=data.updated_at,
        permissions=[
            PermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in data.permissions
        ]
    )
    return MsgRoleResponse(msg="✅ Rol actualizado exitosamente.", data=data)

#! PERMISSIONS


@rtr_role.post("/role/{id}/permission/{id_permission}", response_model=MsgRoleResponse, status_code=status.HTTP_201_CREATED, name="Role - Add Permission 🆗")
async def c(id: int, id_permission: int, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se agrega el permiso al rol.
    """
    data = add_role_permission(db, id, id_permission)
    res = RoleResponse(
        id=data.id,
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        created_at=data.created_at,
        updated_at=data.updated_at,
        permissions=[
            PermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in data.permissions
        ]
    )
    return MsgRoleResponse(msg="✅ Permiso agregado exitosamente.", data=res)


@rtr_role.delete("/role/{id}/permission/{id_permission}", response_model=MsgRoleResponse, status_code=status.HTTP_200_OK, name="Role - Remove Permission 🆗")
async def d(id: int, id_permission: int, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se elimina el permiso al rol.
    """
    data = remove_role_permission(db, id, id_permission)
    res = RoleResponse(
        id=data.id,
        name=data.name,
        description=data.description,
        is_active=data.is_active,
        created_at=data.created_at,
        updated_at=data.updated_at,
        permissions=[
            PermissionResponse(
                id=permission.id,
                name=permission.name,
                description=permission.description,
                created_at=permission.created_at,
                updated_at=permission.updated_at
            )
            for permission in data.permissions
        ]
    )
    return MsgRoleResponse(msg="✅ Permiso eliminado exitosamente.", data=res)
