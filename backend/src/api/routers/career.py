from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from src.api.schemas.career import MsgCareerResponse, CareerResponse, CreateCareer, UpdateCareer, PublicCareerResponse, MsgPublicCareerResponse
from sqlalchemy.orm import Session
from src.api.controllers.career import get_all, get_by_id, create, update
from src.core.connection import DatabaseManager
from src.auth.current import current_user, UserResponse

db_manager = DatabaseManager()

rtr_career = APIRouter(
    prefix="/career",
    tags=["Carreras ✅"]
)

@rtr_career.get("/public/career", response_model=List[CareerResponse], status_code=status.HTTP_200_OK, name="Careers - Get All 🆗")
async def p_r_all(db: Session = Depends(db_manager.get_db)):
    """
    Se obtienen todas las carreras del sistema.
    """
    data = get_all(db)
    #! FILTRAR POR ACTIVO TRUE/FALSE
    data = [
                CareerResponse(
                    id=career.id,
                    code=career.code,
                    name=career.name,
                    description=career.description
                )
                for career in data
            ]
    return data

@rtr_career.get("/public/career/{id}", response_model=MsgPublicCareerResponse, status_code=status.HTTP_200_OK, name="Career - Get By ID 🆗")
async def r(id: int, db: Session = Depends(db_manager.get_db)):
    """
    Se obtiene una carrera por su ID.
    """
    data = get_by_id(db, id)
    if data.is_active == False:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "🔴 Error de busqueda.",
                    "errors": "No se encontró la carrera."
                }
            )
    data = CareerResponse(
                id=data.id,
                code=data.code,
                name=data.name,
                description=data.description,
                url_image=data.url_image,
                url_video=data.url_video,
                url_web=data.url_web,
                is_active=data.is_active
            )
    return MsgCareerResponse(msg="✅ La Carrera se ha obtenido exitosamente.", data=data)

@rtr_career.post("/career", response_model=MsgCareerResponse, status_code=status.HTTP_201_CREATED, name="Career - Create 🆗")
async def c(career: CreateCareer, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se crea una nueva carrera.
    """
    data = create(db, career)
    data = CareerResponse(
                id=data.id,
                code=data.code,
                name=data.name,
                description=data.description,
                url_image=data.url_image,
                url_video=data.url_video,
                url_web=data.url_web,
                is_active=data.is_active
            )
    return MsgCareerResponse(msg="✅ La Carrera se ha creado exitosamente.", data=data)

@rtr_career.get("/career", response_model=List[CareerResponse], status_code=status.HTTP_200_OK, name="Careers - Get All 🆗")
async def r_all(db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se obtienen todas las carreras del sistema.
    """
    data = get_all(db)
    data = [
                CareerResponse(
                    id=career.id,
                    code=career.code,
                    name=career.name,
                    description=career.description,
                    url_image=career.url_image,
                    url_video=career.url_video,
                    url_web=career.url_web,
                    is_active=career.is_active
                )
                for career in data
            ]
    return data

@rtr_career.get("/career/{id}", response_model=MsgCareerResponse, status_code=status.HTTP_200_OK, name="Career - Get By ID 🆗")
async def r(id: int, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se obtiene una carrera por su ID.
    """
    data = get_by_id(db, id)
    data = CareerResponse(
                id=data.id,
                code=data.code,
                name=data.name,
                description=data.description,
                url_image=data.url_image,
                url_video=data.url_video,
                url_web=data.url_web,
                is_active=data.is_active
            )
    return MsgCareerResponse(msg="✅ La Carrera se ha obtenido exitosamente.", data=data)

@rtr_career.put("/career/{id}", response_model=MsgCareerResponse, status_code=status.HTTP_200_OK, name="Career - Update 🆗")
async def u(id: int, career: UpdateCareer, db: Session = Depends(db_manager.get_db), current_user: UserResponse = Depends(current_user)):
    """
    Se actualiza una carrera por su ID.
    """
    data = update(db, id, career)
    data = CareerResponse(
                id=data.id,
                code=data.code,
                name=data.name,
                description=data.description,
                url_image=data.url_image,
                url_video=data.url_video,
                url_web=data.url_web,
                is_active=data.is_active
            )
    return MsgCareerResponse(msg="✅ La Carrera se ha actualizado exitosamente.", data=data)