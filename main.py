from fastapi import FastAPI, Request, HTTPException, Depends, status, WebSocket
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from src.infraestructure.adapters.data_sources.config.database import startup, shutdown, get_db, get_status_api
from src.infraestructure.adapters.data_sources.config.default_data import generate_default_data_tables
from src.infraestructure.adapters.data_sources.config.settings import get_settings

#! MODELS PARA CREAR
from src.infraestructure.adapters.data_sources.models.activity_attendance import ActivityAttendance
from src.infraestructure.adapters.data_sources.models.activity_contract import ActivityContract
from src.infraestructure.adapters.data_sources.models.activity import Activity
from src.infraestructure.adapters.data_sources.models.application import Application
from src.infraestructure.adapters.data_sources.models.budget import Budget
from src.infraestructure.adapters.data_sources.models.contract import Contract
from src.infraestructure.adapters.data_sources.models.default_object_machine_material import DefaultObjectMachineMaterial
from src.infraestructure.adapters.data_sources.models.default_object import DefaultObject
from src.infraestructure.adapters.data_sources.models.detail_application import DetailApplication
from src.infraestructure.adapters.data_sources.models.detail_budget import DetailBudget
from src.infraestructure.adapters.data_sources.models.detail_purchase_rental import DetailPurchaseRental
from src.infraestructure.adapters.data_sources.models.file_project import FileProject
from src.infraestructure.adapters.data_sources.models.incidence_worker import IncidenceWorker
from src.infraestructure.adapters.data_sources.models.incidence import Incidence
from src.infraestructure.adapters.data_sources.models.machine_material_project import MachineMaterialProject
from src.infraestructure.adapters.data_sources.models.machine_material import MachineMaterial
from src.infraestructure.adapters.data_sources.models.machine_project import MachineProject
from src.infraestructure.adapters.data_sources.models.movement import Movement
from src.infraestructure.adapters.data_sources.models.object_machine_material import ObjectMachineMaterial
from src.infraestructure.adapters.data_sources.models.object import Object
from src.infraestructure.adapters.data_sources.models.permission_role import PermissionRole
from src.infraestructure.adapters.data_sources.models.project import Project
from src.infraestructure.adapters.data_sources.models.proposal import Proposal
from src.infraestructure.adapters.data_sources.models.purchase_rental_application import PurchaseRentalApplication
from src.infraestructure.adapters.data_sources.models.purchase_rental import PurchaseRental
from src.infraestructure.adapters.data_sources.models.sub_activity_incidence import SubActivityIncidence
from src.infraestructure.adapters.data_sources.models.sub_activity_object import SubActivityObject
from src.infraestructure.adapters.data_sources.models.sub_activity_worker import SubActivityWorker
from src.infraestructure.adapters.data_sources.models.sub_activity import SubActivity
from src.infraestructure.adapters.data_sources.models.supplier_catalog import SupplierCatalog
from src.infraestructure.adapters.data_sources.models.supplier_category import SupplierCategory
from src.infraestructure.adapters.data_sources.models.supplier import Supplier
from src.infraestructure.adapters.data_sources.models.table_table import TableTable
from src.infraestructure.adapters.data_sources.models.token import Token
from src.infraestructure.adapters.data_sources.models.user import User
from src.infraestructure.adapters.data_sources.models.worker import Worker

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=f"""
                {settings.APP_NAME} ✅
                Docs: <a href="/docs">/docs</a>
                Redoc: <a href="/redoc">/redoc</a>

                ### Features:
                - FastAPI
                - SQLAlchemy
                - MySQL
                - JWT Authentication
                - CRUD operations
                - High performance
                - Architecture Hexagonal

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

#app.mount("/static", StaticFiles(directory="src/infraestructure/static"), name="static")
#templates = Jinja2Templates(directory="src/infraestructure/templates")

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request, db: Session = Depends(get_db)):
    generate_default_data_tables(db)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/healthcheck", status_code=status.HTTP_200_OK, include_in_schema=False)
async def health():
    status_bool = get_status_api()
    if status_bool is True:
        return {"msg": "OK"}
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API is not ready")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")