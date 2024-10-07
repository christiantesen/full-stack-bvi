from fastapi import APIRouter, Depends, status
from typing import List
from src.api.schemas.role import MsgRoleResponse, RoleResponse, CreateRole, UpdateRole
from sqlalchemy.orm import Session
from src.core.connection import get_db
from src.api.controllers.role import get_all, get_by_id, create, update

rtr_role = APIRouter(
    prefix="/role",
    tags=["Roles ✅"]
)

@rtr_role.post("/role", response_model=MsgRoleResponse, status_code=status.HTTP_201_CREATED, name="Role - Create 🆗")
async def c(role: CreateRole, db: Session = Depends(get_db)):
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
                updated_at=data.updated_at
            )
    return MsgRoleResponse(msg="✅ El Rol se ha creado exitosamente.", data=data)

@rtr_role.get("/roles", response_model=List[RoleResponse], status_code=status.HTTP_200_OK, name="Roles - Get All 🆗")
async def r_all(db: Session = Depends(get_db)):
    """
    Se obtienen todos los roles del sistema.
    """
    data = get_all(db)
    data = [
                RoleResponse(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    is_active=role.is_active,
                    created_at=role.created_at,
                    updated_at=role.updated_at
                )
                for role in data
            ]
    return data

@rtr_role.get("/role/{id}", response_model=MsgRoleResponse, status_code=status.HTTP_200_OK, name="Role - Get By ID 🆗")
async def r(id: int, db: Session = Depends(get_db)):
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
                updated_at=data.updated_at
            )
    return MsgRoleResponse(msg="✅ Rol encontrado exitosamente.", data=data)

@rtr_role.put("/role/{id}", response_model=MsgRoleResponse, status_code=status.HTTP_200_OK, name="Role - Update 🆗")
async def u(id: int, role: UpdateRole, db: Session = Depends(get_db)):
    """
    Se actualiza un rol por su ID.
    """
    data = update(db, id, role)
    return MsgRoleResponse(msg="✅ Rol actualizado exitosamente.", data=data)