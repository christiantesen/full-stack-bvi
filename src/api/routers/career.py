from fastapi import APIRouter, Depends, status
from typing import List
from src.api.schemas.career import MsgCareerResponse, CareerResponse, CreateCareer, UpdateCareer
from sqlalchemy.orm import Session
from src.core.connection import get_db
from src.api.controllers.career import get_all, get_by_id, create, update

rtr_career = APIRouter(
    prefix="/career",
    tags=["Carreras ✅"]
)

@rtr_career.post("/career", response_model=MsgCareerResponse, status_code=status.HTTP_201_CREATED, name="Career - Create 🆗")
async def c(career: CreateCareer, db: Session = Depends(get_db)):
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

@rtr_career.get("/careers", response_model=List[CareerResponse], status_code=status.HTTP_200_OK, name="Careers - Get All 🆗")
async def r_all(db: Session = Depends(get_db)):
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
async def r(id: int, db: Session = Depends(get_db)):
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
async def u(id: int, career: UpdateCareer, db: Session = Depends(get_db)):
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