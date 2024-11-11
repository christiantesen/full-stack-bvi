from fastapi import APIRouter, Depends, status
from typing import List
from src.api.schemas.module import MsgModuleResponse, ModuleResponse, CreateModule, UpdateModule
from src.api.schemas.permission import MsgPermissionResponse, PermissionResponse, CreatePermission, UpdatePermission
from sqlalchemy.orm import Session
from src.api.controllers.module import get_all, get_by_id, create, update\
    , create_permission, get_by_id_permission, update_permission
from src.core.connection import DatabaseManager

db_manager = DatabaseManager()

rtr_module = APIRouter(
    prefix="/module",
    tags=["Modules[Permissions] ✅"]
)

#! MODULOS
@rtr_module.post("/module", response_model=MsgModuleResponse, status_code=status.HTTP_201_CREATED, name="Module - Create 🆗")
async def c(module: CreateModule, db: Session = Depends(db_manager.get_db)):
    """
    Se crea un nuevo módulo.
    """
    data = create(db, module)
    data = ModuleResponse(
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
    return MsgModuleResponse(msg="✅ El Módulo se ha creado exitosamente.", data=data)

@rtr_module.get("/modules", response_model=List[ModuleResponse], status_code=status.HTTP_200_OK, name="Modules - Get All 🆗")
async def r_all(db: Session = Depends(db_manager.get_db)):
    """
    Se obtienen todos los módulos del sistema.
    """
    data = get_all(db)
    data = [
                ModuleResponse(
                    id=module.id,
                    name=module.name,
                    description=module.description,
                    is_active=module.is_active,
                    created_at=module.created_at,
                    updated_at=module.updated_at,
                    permissions=[
                        PermissionResponse(
                            id=permission.id,
                            name=permission.name,
                            description=permission.description,
                            created_at=permission.created_at,
                            updated_at=permission.updated_at
                        )
                        for permission in module.permissions
                    ]
                )
                for module in data
            ]
    return data

@rtr_module.get("/module/{id}", response_model=MsgModuleResponse, status_code=status.HTTP_200_OK, name="Module - Get By ID 🆗")
async def r(id: int, db: Session = Depends(db_manager.get_db)):
    """
    Se obtiene un módulo por su ID.
    """
    data = get_by_id(db, id)
    data = ModuleResponse(
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
    return MsgModuleResponse(msg="✅ Módulo recuperado exitosamente.", data=data)

@rtr_module.put("/module/{id}", response_model=MsgModuleResponse, status_code=status.HTTP_200_OK, name="Module - Update 🆗")
async def u(id: int, module: UpdateModule, db: Session = Depends(db_manager.get_db)):
    """
    Se actualiza un módulo por su ID.
    """
    data = update(db, id, module)
    data = ModuleResponse(
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
    return MsgModuleResponse(msg="✅ Módulo actualizado exitosamente.", data=data)

#! PERMISOS
@rtr_module.post("/module/{id}/permission", response_model=MsgModuleResponse, status_code=status.HTTP_201_CREATED, name="Module[Permission] - Create 🆗")
async def c_p(id: int, permission: CreatePermission, db: Session = Depends(db_manager.get_db)):
    """
    Se crea un nuevo permiso en un módulo.
    """
    data = create_permission(db, id, permission)
    data = ModuleResponse(
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
    return MsgModuleResponse(msg="✅ El Permiso se ha creado exitosamente.", data=data)

@rtr_module.get("/module/permission/{id}", response_model=MsgPermissionResponse, status_code=status.HTTP_200_OK, name="Module[Permission] - Get By ID 🆗")
async def r_all_p(id: int, db: Session = Depends(db_manager.get_db)):
    """
    Se obtienen todos los permisos de un módulo.
    """
    data = get_by_id_permission(db, id)
    res = PermissionResponse(
                    id=data.id,
                    name=data.name,
                    description=data.description,
                    created_at=data.created_at,
                    updated_at=data.updated_at
                )
    return MsgPermissionResponse(msg="✅ Permiso recuperado exitosamente.", data=res)

@rtr_module.put("/module/permission/{id}", response_model=MsgModuleResponse, status_code=status.HTTP_200_OK, name="Module[Permission] - Update 🆗")
async def u_p(id: int, permission: UpdatePermission, db: Session = Depends(db_manager.get_db)):
    """
    Se actualiza un permiso por su ID.
    """
    data = update_permission(db, id, permission)
    data = ModuleResponse(
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
    return MsgModuleResponse(msg="✅ Permiso actualizado exitosamente.", data=data)