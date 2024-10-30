from fastapi import FastAPI, Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.src.core.connection import DatabaseManager#startup, shutdown, get_db, get_status_api
from backend.src.core.settings import get_settings

settings = get_settings()
db_manager = DatabaseManager()

app = FastAPI(
    title=settings.APP_NAME,
    description=f"""
                {settings.APP_NAME} ✅
                Estanteria Virtual
                ### Features:
                - Admin Panel
                - 

                2024 © All rights reserved. {settings.APP_NAME} API
                """,
    version="0.0.1",
    debug=settings.DEBUG,
    summary="Hyre"
)
# if configuraciones.BACKEND_CORS_ORIGINS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/src/core/static"), name="static")
templates = Jinja2Templates(directory="backend/src/core/templates")

app.add_event_handler("startup", db_manager.startup)
app.add_event_handler("shutdown", db_manager.shutdown)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request, db: Session = Depends(db_manager.get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hc", status_code=status.HTTP_200_OK, include_in_schema=False)
async def health():
    status_bool = db_manager.get_status_api()
    if status_bool is True:
        return {"msg": "OK 🆗"}
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Offline 🔴")

#! ROUTERS
from backend.src.api.routers import role, career, user

app.include_router(role.rtr_role)
app.include_router(career.rtr_career)
app.include_router(user.rtr_user)
