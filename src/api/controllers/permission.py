from src.core.models.permission import Permission as permission_model
from src.api.schemas.permission import CreatePermission, UpdatePermission
from fastapi import HTTPException, status
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR

def get_by_id(db, id: int):
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
        
def permission_name_exits(db, name: str, module_id: int, id: int = None):
    try:
        permission = None
        if id:
            permission = db.query(permission_model).filter(permission_model.name == name, permission_model.module_id == module_id, permission_model.id != id).first()
        else:
            permission = db.query(permission_model).filter(permission_model.name == name, permission_model.module_id == module_id).first()
        if permission:
            hyre.warning("Permission name exists")
            return True
        hyre.info("Permission name does not exist")
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
        
def create(db, permission: CreatePermission):
    try:
        if permission_name_exits(db, permission.name, permission.module_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del permiso ya existe."]
                }
            )
        permission = permission_model(**permission.dict())
        db.add(permission)
        db.commit()
        db.refresh(permission)
        hyre.success("Permission created successfully")
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
        
def update(db, permission: UpdatePermission):
    try:
        permission_db = get_by_id(db, permission.id)
        if permission_name_exits(db, permission.name, permission_db.module_id, permission.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del permiso ya existe."]
                }
            )
        permission_db.name = permission.name
        permission_db.description = permission.description
        db.commit()
        db.refresh(permission_db)
        hyre.success("Permission updated successfully")
        return permission_db
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