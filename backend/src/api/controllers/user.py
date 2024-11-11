from src.core.models.user import User as user_model
from src.api.schemas.user import CreateUser, UpdateUser
from fastapi import HTTPException, status
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR
from src.security.pwd import PasswordManager
from src.api.controllers.role import get_by_id as get_role_by_id
from src.api.controllers.career import get_by_id as get_career_by_id

pm = PasswordManager()


def get_all(db):
    try:
        users = db.query(user_model).all()
        for user in users:
            user.role = get_role_by_id(db, user.role_id)
            user.career = get_career_by_id(db, user.career_id) if user.career_id else None
        hyre.success("Users retrieved successfully")
        return users
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
    try:
        user = db.query(user_model).filter(user_model.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Usuario no encontrado."]
                }
            )
        user.role = get_role_by_id(db, user.role_id)
        user.career = get_career_by_id(db, user.career_id) if user.career_id else None
        hyre.success("User retrieved from database")
        return user
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


def username_exists(db, username: str, id: int = None) -> bool:
    try:
        user = None
        if id:
            user = db.query(user_model).filter(
                user_model.username == username, user_model.id != id).first()
        else:
            user = db.query(user_model).filter(
                user_model.username == username).first()
        if user:
            hyre.warning("Username exists")
            return True
        hyre.info("Username does not exist")
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


def create_1_2(db, user: CreateUser):
    if username_exists(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "🔴 Error de validación.",
                "errors": ["El nombre de usuario ya existe."]
            }
        )
    try:
        if user.role_id not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "🔴 Error de validación.",
                    "errors": ["El rol de usuario no es válido."]
                }
            )
        new_user = user_model(
            username=user.username,
            password=pm.hash_password(user.password),
            full_name=user.full_name,
            paternal_name=user.paternal_name,
            maternal_name=user.maternal_name,
            email=user.email,
            phone=user.phone,
            career_id=user.career_id,
            role_id=user.role_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        hyre.success("User created successfully")
        return new_user
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
        
def create_3_4(db, user: CreateUser):
    if username_exists(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "msg": "🔴 Error de validación.",
                "errors": ["El nombre de usuario ya existe."]
            }
        )
    try:
        if user.role_id not in [3, 4]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "🔴 Error de validación.",
                    "errors": ["El rol de usuario no es válido."]
                }
            )
        new_user = user_model(
            username=user.username,
            password=pm.hash_password(user.password),
            full_name=user.full_name,
            paternal_name=user.paternal_name,
            maternal_name=user.maternal_name,
            email=user.email,
            phone=user.phone,
            career_id=user.career_id,
            role_id=user.role_id
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        hyre.success("User created successfully")
        return new_user
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


def update(db, id: int, user: UpdateUser):
    try:
        if username_exists(db, user.username, id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "🔴 Error de validación.",
                    "errors": ["El nombre de usuario ya existe."]
                }
            )

        user = db.query(user_model).filter(user_model.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "msg": "🔴 Error de búsqueda.",
                    "errors": ["Usuario no encontrado."]
                }
            )
        user.password = user.password if not user.password else user.password
        user.full_name = user.full_name if not user.full_name else user.full_name
        user.paternal_name = user.paternal_name if not user.paternal_name else user.paternal_name
        user.maternal_name = user.maternal_name if not user.maternal_name else user.maternal_name
        user.email = user.email if not user.email else user.email
        user.phone = user.phone if not user.phone else user.phone
        user.is_active = user.is_active if not user.is_active else user.is_active
        user.is_blocked = user.is_blocked if not user.is_blocked else user.is_blocked
        user.career_id = user.career_id if not user.career_id else user.career_id
        user.role_id = user.role_id if not user.role_id else user.role_id
        db.commit()
        db.refresh(user)
        hyre.success("User updated successfully")
        return user
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
