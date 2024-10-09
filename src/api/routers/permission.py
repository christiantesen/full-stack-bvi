from fastapi import APIRouter, Depends, status
from typing import List
from src.api.schemas.permission import MsgPermissionResponse, PermissionResponse, CreatePermission, UpdatePermission
from sqlalchemy.orm import Session
from src.core.connection import get_db
from src.api.controllers.permission import get_by_id, create, update

rtr_permission = APIRouter(
    prefix="/permission",
    tags=["Permissions ✅"]
)

@rtr_permission.post("/permission", response_model=MsgPermissionResponse, status_code=status.HTTP_201_CREATED, name="Permission - Create 🆗")
async def c(permission: CreatePermission, db: Session = Depends(get_db)):
    """
    Se crea un nuevo permiso.
    """
    data = create(db, permission)
    data = PermissionResponse(
                id=data.id,
                name=data.name,
                description=data.description,
                created_at=data.created_at,
                updated_at=data.updated_at,
                module_id=data.module_id
            )
    return MsgPermissionResponse(msg="✅ El Permiso se ha creado exitosamente.", data=data)

@rtr_permission.get("/permission/{id}", response_model=MsgPermissionResponse, status_code=status.HTTP_200_OK, name="Permission - Get By ID 🆗")
async def r(id: int, db: Session = Depends(get_db)):
    """
    Se obtiene un permiso por su ID.
    """
    data = get_by_id(db, id)
    data = PermissionResponse(
                id=data.id,
                name=data.name,
                description=data.description,
                created_at=data.created_at,
                updated_at=data.updated_at,
                module_id=data.module_id
            )
    return MsgPermissionResponse(msg="✅ El Permiso se ha encontrado exitosamente.", data=data)

@rtr_permission.put("/permission/{id}", response_model=MsgPermissionResponse, status_code=status.HTTP_200_OK, name="Permission - Update 🆗")
async def u(id: int, permission: UpdatePermission, db: Session = Depends(get_db)):
    """
    Se actualiza un permiso por su ID.
    """
    data = update(db, id, permission)
    data = PermissionResponse(
                id=data.id,
                name=data.name,
                description=data.description,
                created_at=data.created_at,
                updated_at=data.updated_at,
                module_id=data.module_id
            )
    return MsgPermissionResponse(msg="✅ El Permiso se ha actualizado exitosamente.", data=data)