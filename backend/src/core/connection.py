from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator
from src.core.settings import get_settings
from src.utils.logger import hyre
from sqlalchemy.orm import Session
import json

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URI,  # ? URI de la base de datos.
    pool_size=200,  # ? 200 Conexiones en el pool
    pool_pre_ping=True,  # ? Chequear las conexiones antes de usarlas
    pool_recycle=3600,  # ? Reciclar las conexiones después de 1 hora
    max_overflow=0,  # ? No permitir conexiones adicionales
    
)
# ? Crear una sesión de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ? Crear una sesión de base de datos con alcance.
ScopedSession = scoped_session(SessionLocal)
# ? Clase base para las clases de modelo de SQLAlchemy.
Base = declarative_base()
status_api = None  # ? Variable para almacenar el estado de la API.

def get_db() -> Generator:
    db = ScopedSession()  # Crear la sesión de base de datos
    try:
        yield db  # Proporcionar la sesión para su uso
    except SQLAlchemyError as e:
        db.rollback()  # Deshacer cambios si ocurre un error
        hyre.critical(f"Database error occurred: {e}")  # Registrar con el stack trace
        raise  # Re-lanzar la excepción para que sea manejada a nivel superior
    finally:
        db.close()  # Cerrar siempre la sesión


async def startup():
    """
    Start the API
    """
    global status_api
    hyre.info("🛑 Loading API 🛑")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if not tables:
        create_tables()
    else:
        drop_tables()
        await startup()
    await default_data()
    hyre.success("🆗 API started 🆗")
    status_api = True


def shutdown():
    """
    Shutdown the API
    """
    global status_api
    hyre.info("🛑 Closing API 🛑")
    if engine is not None:
        engine.dispose()
    status_api = False
    hyre.info("🆗 API closed 🆗")


def get_status_api():
    """
    Get the status of the API

    Returns:
        bool: The status of the API
    """
    return status_api


def get_tables():
    """
    Get the tables in the database

    Returns:
        list: The tables in the database
    """
    inspector = inspect(engine)
    tables = {}
    for table_name in inspector.get_table_names():
        columns = []
        for column in inspector.get_columns(table_name):
            columns.append({
                "name": column["name"],
                "type": str(column["type"])
            })
        tables[table_name] = columns
    return tables


def create_tables():
    """
    Create the tables in the database
    """
    Base.metadata.create_all(bind=engine)
    hyre.info("✅ Created tables ✅")

def drop_tables():
    """
    Drop the tables in the database
    """
    Base.metadata.drop_all(bind=engine)
    hyre.info("✅ Droped tables ✅")



async def default_data():
    with ScopedSession() as db:
        try:
            insert_careers(db)
            insert_roles(db)
        except SQLAlchemyError as e:
            hyre.critical(f"Database error occurred: {e}")
            raise
        
def insert_careers(db: Session):
    from src.core.models import career
    
    # Lee los datos del archivo JSON
    try:
        if db.query(career.Career).count() == 0:
            with open('src/core/data/career.json', 'r') as file:
                career_data = json.load(file)
                insert_data(db, career.Career, career_data['careers'])
    except FileNotFoundError:
        hyre.critical("El archivo career.json no fue encontrado.")
        raise
    except json.JSONDecodeError as e:
        hyre.critical(f"Error al decodificar el archivo JSON: {e}")
        raise
    
def insert_roles(db: Session):
    from src.core.models import role
    
    # Lee los datos del archivo JSON
    try:
        if db.query(role.Role).count() == 0:
            with open('src/core/data/role.json', 'r') as file:
                role_data = json.load(file)
                insert_data(db, role.Role, role_data['roles'])
    except FileNotFoundError:
        hyre.critical("El archivo role.json no fue encontrado.")
        raise
    except json.JSONDecodeError as e:
        hyre.critical(f"Error al decodificar el archivo JSON: {e}")
        raise

# Función para insertar datos en bloques
def insert_data(db, model, data):
    try:
        db.bulk_insert_mappings(model, data)  # Inserta los datos en bloques
        db.commit()  # Confirma la transacción
        hyre.success("Datos insertados correctamente.")
    except SQLAlchemyError as e:
        db.rollback()  # En caso de error, deshace la transacción
        hyre.critical(f"Database error occurred: {e}")
        raise