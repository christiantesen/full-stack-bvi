from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator
from src.infraestructure.adapters.data_sources.config.settings import get_settings
from fastapi.logger import logger
from contextlib import contextmanager

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

@contextmanager
def get_db():
    db = ScopedSession()
    try:
        yield db
    db = scoped_session()  # Crear la sesión de base de datos
    try:
        yield db  # Proporcionar la sesión para su uso
    except SQLAlchemyError as e:
        db.rollback()  # Deshacer cambios si ocurre un error
        logger.exception(f"Database error occurred: {e}")  # Registrar con el stack trace
        raise  # Re-lanzar la excepción para que sea manejada a nivel superior
    finally:
        db.close()  # Cerrar siempre la sesión


def startup():
    """
    Start the API
    """
    global status_api
    logger.info("Loading API 🛑")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if not tables:
        create_tables()
    else:
        drop_tables()
        startup()
    logger.info("API started 🆗")
    status_api = True


def shutdown():
    """
    Shutdown the API
    """
    global status_api
    logger.info("Closing API 🛑")
    if engine is not None:
        engine.dispose()
    status_api = False
    logger.info("API closed 🆗")


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
    logger.info("Created tables ✅")


def drop_tables():
    """
    Drop the tables in the database
    """
    Base.metadata.drop_all(bind=engine)
    logger.info("Droped tables ✅")