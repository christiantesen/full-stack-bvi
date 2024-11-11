from src.core.models.role import Role as role_model
from src.core.models.permission import Permission as permission_model
from src.core.models.role_permission import RolePermission as role_permission_model
from src.api.schemas.role import CreateRole, UpdateRole
from fastapi import HTTPException, status
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR
from . import CACHE_ROLES

#! INTERNALS


def internal_permission_get_by_id(db, id: int):
    try:
        permission = db.query(permission_model).filter(
            permission_model.id == id).first()
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
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


def internal_get_by_id(db, id: int):
    try:
        role = db.query(role_model).filter(role_model.id == id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Rol no encontrado."]
                }
            )
        return role
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


def internal_get_by_name(db, name: str, id: int = None) -> bool:
    try:
        role = None
        if id:
            role = db.query(role_model).filter(
                role_model.name == name, role_model.id != id).first()
        else:
            role = db.query(role_model).filter(role_model.name == name).first()
        if role:
            hyre.warning("Role name exists")
            return True
        hyre.info("Role name does not exist")
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

#! ROLES


def get_all(db):
    global CACHE_ROLES
    try:
        # Si no hay roles en caché, se consultan de la base de datos
        if not CACHE_ROLES:
            CACHE_ROLES = db.query(role_model).all()
            for role in CACHE_ROLES:
                permissions = []
                role_permission = db.query(role_permission_model).filter(
                    role_permission_model.role_id == role.id).all()
                for rp in role_permission:
                    permission = db.query(permission_model).filter(
                        permission_model.id == rp.permission_id).first()
                    permissions.append(permission)
                role.permissions = permissions
            hyre.info("Cache roles updated successfully")
        hyre.success("Roles retrieved from cache successfully")
        return CACHE_ROLES
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
    global CACHE_ROLES
    # Si cache_roles está vacío, se consultan todos los roles
    if not CACHE_ROLES:
        get_all(db)
    # Comprobar si el rol está en caché
    role = next((role for role in CACHE_ROLES if role.id == id), None)
    if role:
        hyre.success("Role retrieved from cache successfully")
        return role
    role = internal_get_by_id(db, id) 
    try:
        permissions = []
        role_permission = db.query(role_permission_model).filter(
            role_permission_model.role_id == role.id).all()
        for rp in role_permission:
            permission = db.query(permission_model).filter(
                permission_model.id == rp.permission_id).first()
            permissions.append(permission)
        role.permissions = permissions
        # Agregar el nuevo rol a la caché
        CACHE_ROLES.append(role)
        hyre.info("Cache roles updated successfully")
        hyre.success("Role retrieved from database")
        return role
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


def create(db, role: CreateRole):
    if internal_get_by_name(db, role.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "🔴 Error de validación.",
                "errors": ["El nombre del rol ya existe."]
            }
        )
    try:
        new_role = role_model(
            name=role.name,
            description=role.description
        )
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        new_role.permissions = []
        # Invalida el caché al crear un nuevo rol
        CACHE_ROLES.append(new_role)
        hyre.info("Cache roles updated successfully")
        hyre.success("Role created successfully")
        return new_role
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


def update(db, id: int, role: UpdateRole):
    global CACHE_ROLES
    role = internal_get_by_id(db, id)
    if internal_get_by_name(db, role.name, id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "🔴 Error de validación.",
                "errors": ["El nombre del rol ya existe."]
            }
        )
    try:
        role.name = role.name
        role.description = role.description
        role.is_active = role.is_active
        db.commit()
        db.refresh(role)
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
    # Actualiza el caché de roles
    CACHE_ROLES = [role for role in CACHE_ROLES if role.id != id]
    hyre.info("Cache roles updated successfully")
    hyre.success("Role updated successfully")
    return get_by_id(db, id)

#! ROLES PERMISSIONS


def add_role_permission(db, role_id: int, permission_id: int):
    global CACHE_ROLES
    internal_get_by_id(db, role_id)
    internal_permission_get_by_id(db, permission_id)
    try:
        role_permission_exists = db.query(role_permission_model).filter(
            role_permission_model.role_id == role_id,
            role_permission_model.permission_id == permission_id
        ).first()
        if role_permission_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "🔴 Error de validación.",
                    "errors": ["El permiso ya está asignado al rol."]
                }
            )
        role_permission = role_permission_model(
            role_id=role_id,
            permission_id=permission_id
        )
        db.add(role_permission)
        db.commit()
        db.refresh(role_permission)
        hyre.success("Role permission created successfully")
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
    # Actualiza el caché de roles
    CACHE_ROLES = [role for role in CACHE_ROLES if role.id != role_id]
    return get_by_id(db, role_id)


def remove_role_permission(db, role_id: int, permission_id: int):
    global CACHE_ROLES
    internal_get_by_id(db, role_id)
    internal_permission_get_by_id(db, permission_id)
    try:
        role_permission = db.query(role_permission_model).filter(
            role_permission_model.role_id == role_id,
            role_permission_model.permission_id == permission_id
        ).first()
        if not role_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Permiso no encontrado."]
                }
            )
        db.delete(role_permission)
        db.commit() 
        hyre.success("Role permission deleted successfully")
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
    # Actualiza el caché de roles
    CACHE_ROLES = [role for role in CACHE_ROLES if role.id != role_id]
    return get_by_id(db, role_id)
