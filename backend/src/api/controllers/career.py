from src.core.models.career import Career as career_model
from src.api.schemas.career import CreateCareer, UpdateCareer
from fastapi import HTTPException, status
from src.utils.logger import hyre, MSG_INTERNAL_SERVER_ERROR

CACHE_CAREERS = []

def get_all(db):
    global CACHE_CAREERS
    try:
        # Si no hay carreras en caché, se consultan de la base de datos
        if not CACHE_CAREERS:
            CACHE_CAREERS = db.query(career_model).all()
            hyre.info("Cache careers updated successfully")
        hyre.success("Careers retrieved from cache successfully")
        return CACHE_CAREERS
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
    global CACHE_CAREERS
    # Si cache_careers está vacío, se consultan todas las carreras
    if not CACHE_CAREERS:
        get_all(db)
    try:
        # Comprobar si la carrera está en caché
        career = next((career for career in CACHE_CAREERS if career.id == id), None)
        if career:
            hyre.success("Career retrieved from cache successfully")
            return career
        # Si no está en caché, se consulta de la base de datos
        career = db.query(career_model).filter(career_model.id == id).first()
        if not career:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=
                {
                    "msg": "🔴 Carrera no encontrada.",
                    "errors": []
                }
            )
        # Agregar la nueva carrera a la caché
        CACHE_CAREERS.append(career)
        hyre.info("Cache careers updated successfully")
        hyre.success("Career retrieved from database")
        return career
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
        
def career_code_exists(db, code: str, id: int = None) -> bool:
    try:
        career = None
        if id:
            career = db.query(career_model).filter(career_model.code == code, career_model.id != id).first()
        else:
            career = db.query(career_model).filter(career_model.code == code).first()
        if career:
            hyre.success("Career code exists")
            return True
        hyre.success("Career code does not exist")
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
        
def career_name_exists(db, name: str, id: int = None) -> bool:
    try:
        career = None
        if id:
            career = db.query(career_model).filter(career_model.name == name, career_model.id != id).first()
        else:
            career = db.query(career_model).filter(career_model.name == name).first()
        if career:
            hyre.success("Career name exists")
            return True
        hyre.success("Career name does not exist")
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
        
def create(db, career: CreateCareer):
    try:
        errors = []
        if career_code_exists(db, career.code):
            errors.append("El código de la carrera ya existe.")
        if career_name_exists(db, career.name):
            errors.append("El nombre de la carrera ya existe.")
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": errors
                }
            )
        new_career = career_model(
            code=career.code,
            name=career.name,
            description=career.description,
            url_image=career.url_image,
            url_video=career.url_video,
            url_web=career.url_web
        )
        db.add(new_career)
        db.commit()
        db.refresh(new_career)
        CACHE_CAREERS.append(new_career)
        hyre.info("Cache careers updated successfully")
        hyre.success("Career created successfully")
        return new_career
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
        
def update(db, id: int, career: UpdateCareer):
    global CACHE_CAREERS
    get_by_id(db, id)
    try:
        errors = []
        if career_code_exists(db, career.code, id):
            errors.append("El código de la carrera ya existe.")
        if career_name_exists(db, career.name, id):
            errors.append("El nombre de la carrera ya existe.")
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=
                {
                    "msg": "🔴 Error de validación.",
                    "errors": errors
                }
            )
        db.query(career_model).filter(career_model.id == id).update({
            career_model.code: career.code,
            career_model.name: career.name,
            career_model.description: career.description,
            career_model.url_image: career.url_image,
            career_model.url_video: career.url_video,
            career_model.url_web: career.url_web,
            career_model.is_active: career.is_active
        })
        db.commit()
        CACHE_CAREERS = [career for career in CACHE_CAREERS if career.id != id]
        hyre.info("Cache careers updated successfully")
        hyre.success("Career updated successfully")
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