from src.core.models.module import Module as module_model
from sqlalchemy.orm import joinedload
from src.core.models.permission import Permission as permission_model
from src.api.schemas.module import CreateModule, UpdateModule
from fastapi import HTTPException, status
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR

CACHE_MODULES = []

def get_all(db):
    global CACHE_MODULES
    try:
        # Si no hay módulos en caché, se consultan de la base de datos
        if not CACHE_MODULES:
            CACHE_MODULES = db.query(module_model).options(joinedload(module_model.permissions)).all()
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
        module = db.query(module_model).options(joinedload(module_model.permissions)).filter(module_model.id == id).first()
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=
                {
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Módulo no encontrado."]
                }
            )
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
        
def module_name_exits(db, name: str, id: int= None) -> bool:
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
    
def create(db, module: CreateModule):
    try:
        if module_name_exits(db, module.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del módulo ya existe."]
                }
            )
        new_module = module_model(
            name=module.name,
            description=module.description
        )
        db.add(new_module)
        db.commit()
        db.refresh(new_module)
        CACHE_MODULES.append(new_module)
        hyre.info("Cache modules updated successfully")
        hyre.success("Module created successfully")
        return new_module
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
        
def update(db, id: int, module: UpdateModule):
    global CACHE_MODULES    
    get_by_id(db, id)
    try:
        if module_name_exits(db, module.name, id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del módulo ya existe."]
                }
            )
        db.query(module_model).filter(module_model.id == id).update({
            module_model.name: module.name,
            module_model.description: module.description,
            module_model.is_active: module.is_active
        })
        db.commit()
        # Invalida el caché al actualizar un módulo
        CACHE_MODULES = [module for module in CACHE_MODULES if module.id != id]
        hyre.info("Cache modules updated successfully")
        hyre.success("Module updated successfully")
        return get_by_id(db, id)
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