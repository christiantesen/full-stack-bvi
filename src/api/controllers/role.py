from src.core.models.role import Role as role_model
from src.api.schemas.role import CreateRole, UpdateRole
from fastapi import HTTPException, status
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR

CACHE_ROLES = []


def get_all(db):
    global CACHE_ROLES
    try:
        # Si no hay roles en caché, se consultan de la base de datos
        if not CACHE_ROLES:
            CACHE_ROLES = db.query(role_model).all()
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
    try:
        # Comprobar si el rol está en caché
        role = next((role for role in CACHE_ROLES if role.id == id), None)
        if role:
            hyre.success("Role retrieved from cache successfully")
            return role
        # Si no está en caché, se consulta de la base de datos
        role = db.query(role_model).filter(role_model.id == id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=
                {
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Rol no encontrado."]
                }
            )
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


def role_name_exists(db, name: str, id: int = None) -> bool:
    try:
        role = None
        if id:
            role = db.query(role_model).filter(
                role_model.name == name, role_model.id != id).first()
        else:
            role = db.query(role_model).filter(role_model.name == name).first()
        if role:
            hyre.success("Role name exists")
            return True
        hyre.success("Role name does not exist")
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


def create(db, role: CreateRole):
    try:
        if role_name_exists(db, role.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del rol ya existe."]
                }
            )
        new_role = role_model(
            name=role.name,
            description=role.description
        )
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
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
    get_by_id(db, id)
    try:
        if role_name_exists(db, role.name, id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre del rol ya existe."]
                }
            )
        db.query(role_model).filter(role_model.id == id).update({
            role_model.name: role.name,
            role_model.description: role.description,
            role_model.is_active: role.is_active
        })
        db.commit()
        # Invalida el caché al actualizar un rol
        CACHE_ROLES = [role for role in CACHE_ROLES if role.id != id]
        hyre.info("Cache roles updated successfully")
        hyre.success("Role updated successfully")
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
