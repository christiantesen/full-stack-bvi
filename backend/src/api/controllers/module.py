from src.core.models.module import Module as module_model
from src.api.schemas.module import CreateModule, UpdateModule
from src.core.models.permission import Permission as permission_model
from src.api.schemas.permission import CreatePermission, UpdatePermission
from fastapi import HTTPException, status
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR

CACHE_MODULES = []

#! INTERNAL
def internal_get_by_id_permission(db, id: int):
    try:
        permission = db.query(permission_model).filter(permission_model.id == id).first()
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=
                {
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Permiso no encontrado."]
                }
            )
        hyre.success("Permission retrieved successfully")
        return permission
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

def internal_permission_name_exits(db, name: str, id: int= None) -> bool:
    try:
        permission = None
        if id:
            permission = db.query(permission_model).filter(permission_model.name == name, permission_model.id != id).first()
        else:
            permission = db.query(permission_model).filter(permission_model.name == name).first()
        if permission:
            hyre.success("Permission name exists")
            return True
        hyre.warning("Permission name does not exist")
        return False
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

def internal_get_by_id(db, id: int):
    try:
        module = db.query(module_model).filter(module_model.id == id).first()
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=
                {
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Módulo no encontrado."]
                }
            )
        hyre.success("Module retrieved successfully")
        return module
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

def internal_name_exits(db, name: str, id: int= None) -> bool:
    try:
        module = None
        if id:
            module = db.query(module_model).filter(module_model.name == name, module_model.id != id).first()
        else:
            module = db.query(module_model).filter(module_model.name == name).first()
        if module:
            hyre.success("Module name exists")
            return True
        hyre.warning("Module name does not exist")
        return False
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

#! MODULES
def get_all(db):
    global CACHE_MODULES
    try:
        # Si no hay módulos en caché, se consultan de la base de datos
        if not CACHE_MODULES:
            permissions = db.query(permission_model).all()
            CACHE_MODULES = db.query(module_model).all()
            for module in CACHE_MODULES:
                module.permissions = [permission for permission in permissions if permission.module_id == module.id]
            hyre.info("Cache modules updated successfully")
        hyre.success("Modules retrieved from cache successfully")
        return CACHE_MODULES
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
        
def get_by_id(db, id: int):
    global CACHE_MODULES
    # Si cache_modules está vacío, se consultan todos los módulos
    if not CACHE_MODULES:
        get_all(db)
    try:
        # Comprobar si el módulo está en caché
        module = next((module for module in CACHE_MODULES if module.id == id), None)
        if module:
            hyre.success("Module retrieved from cache successfully")
            return module
        # Si no está en caché, se consulta de la base de datos
        module = db.query(module_model).filter(module_model.id == id).first()
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=
                {
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Módulo no encontrado."]
                }
            )
        module.permissions = db.query(permission_model).filter(permission_model.module_id == module.id).all()
        # Agregar el nuevo módulo a la caché
        CACHE_MODULES.append(module)
        hyre.info("Cache modules updated successfully")
        hyre.success("Module retrieved from database")
        return module
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
        

    
def create(db, data: CreateModule):
    try:
        if internal_name_exits(db, data.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del módulo ya existe."]
                }
            )
        module = module_model(
            name=data.name,
            description=data.description
        )
        db.add(module)
        db.commit()
        db.refresh(module)
        module.permissions = []
        CACHE_MODULES.append(module)
        hyre.info("Cache modules updated successfully")
        hyre.success("Module created successfully")
        return module
    except HTTPException as e:
        hyre.error(f"{e.detail}")
        raise e
    except Exception as e:
        hyre.critical(f"{str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": MSG_INTERNAL_SERVER_ERROR,
                "errors": []
            }
        )
        
def update(db, id: int, data: UpdateModule):
    global CACHE_MODULES    
    module = internal_get_by_id(db, id)
    if internal_name_exits(db, module.name, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=
            {
                "msg": "🔴 Error de validación.",
                "errors": ["El nombre del módulo ya existe."]
            }
        )
    try:
        module.name = data.name
        module.description = data.description
        module.is_active = data.is_active    
        db.commit()
        db.refresh(module)
        # Eliminar el módulo de la caché
        CACHE_MODULES = [module for module in CACHE_MODULES if module.id != id]
        hyre.info("Cache modules updated successfully")
        hyre.success("Module updated successfully")
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
    return get_by_id(db, id)

#! PERMISSIONS MODULE
def create_permission(db, id:int, data: CreatePermission):
    global CACHE_MODULES
    internal_get_by_id(db, id)
    try:
        exists = internal_permission_name_exits(db, data.name)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del permiso ya existe."]
                }
            )
        permission = permission_model(
            name=data.name,
            description=data.description,
            module_id=id
        )
        db.add(permission)
        db.commit()
        db.refresh(permission)
        hyre.success("Permission created successfully")
    except HTTPException as e:
        hyre.error(f"{e.detail}")
        raise e
    except Exception as e:
        hyre.critical(f"{str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": MSG_INTERNAL_SERVER_ERROR,
                "errors": []
            }
        )
    # Eliminar el módulo de la caché
    CACHE_MODULES = [module for module in CACHE_MODULES if module.id != id]
    hyre.info("Cache modules updated successfully")
    return get_by_id(db, id)

def get_by_id_permission(db, id: int):
    return internal_get_by_id_permission(db, id)

def update_permission(db, id: int, data: UpdatePermission):
    global CACHE_MODULES
    permission = internal_get_by_id_permission(db, id)
    try:
        permission.name = data.name
        permission.description = data.description
        db.commit()
        db.refresh(permission)
        hyre.success("Permission updated successfully")
    except HTTPException as e:
        hyre.error(f"{e.detail}")
        raise e
    except Exception as e:
        hyre.critical(f"{str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "msg": MSG_INTERNAL_SERVER_ERROR,
                "errors": []
            }
        )
    # Eliminar el módulo de la caché
    CACHE_MODULES = [module for module in CACHE_MODULES if module.id != permission.module_id]
    hyre.info("Cache modules updated successfully")
    return get_by_id(db, permission.module_id)