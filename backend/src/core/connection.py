from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from typing import Generator, List
from sqlalchemy.orm import Session
import json
from backend.src.utils.logger import LoggerConfig
from backend.src.core.settings import get_settings

class DatabaseManager:
    def __init__(self):
        self.logger_config = LoggerConfig()
        self.hyre = self.logger_config.get_logger()
        self.settings = get_settings()
        self.engine = create_engine(
            self.settings.DATABASE_URI,  # URI de la base de datos
            pool_size=200,  # Conexiones en el pool
            pool_pre_ping=True,  # Chequear las conexiones antes de usarlas
            pool_recycle=3600,  # Reciclar las conexiones después de 1 hora
            max_overflow=0,  # No permitir conexiones adicionales
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.ScopedSession = scoped_session(self.SessionLocal)
        Base = declarative_base()
        self.status_api = None  # Estado de la API

    def get_db(self) -> Generator:
        db = self.ScopedSession()  # Crear la sesión de base de datos
        try:
            yield db  # Proporcionar la sesión para su uso
        except SQLAlchemyError as e:
            db.rollback()  # Deshacer cambios si ocurre un error
            self.hyre.critical(f"Database error occurred: {e}")  # Registrar el error
            raise
        finally:
            db.close()  # Cerrar la sesión

    async def startup(self):
        """Inicia la API."""
        global status_api
        self.hyre.info("🛑 Loading API 🛑")
        inspector = inspect(self.engine)
        tables = inspector.get_table_names()
        if not tables:
            self.create_tables()
        else:
            self.drop_tables()
            await self.startup()
        await self.default_data()
        self.hyre.success("🆗 API started 🆗")
        self.status_api = True

    def shutdown(self):
        """Apaga la API."""
        global status_api
        self.hyre.info("🛑 Closing API 🛑")
        if self.engine is not None:
            self.engine.dispose()
        self.status_api = False
        self.hyre.info("🆗 API closed 🆗")

    def get_status_api(self) -> bool:
        """Devuelve el estado de la API."""
        return self.status_api

    def get_tables(self) -> dict:
        """Obtiene las tablas en la base de datos."""
        inspector = inspect(self.engine)
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

    def create_tables(self):
        """Crea las tablas en la base de datos."""
        self.Base.metadata.create_all(bind=self.engine)
        self.hyre.info("✅ Created tables ✅")

    def drop_tables(self):
        """Elimina las tablas en la base de datos."""
        self.Base.metadata.drop_all(bind=self.engine)
        self.hyre.info("✅ Dropped tables ✅")

    async def default_data(self):
        with self.ScopedSession() as db:
            try:
                self.insert_careers(db)
                self.insert_roles(db)
            except SQLAlchemyError as e:
                self.hyre.critical(f"Database error occurred: {e}")
                raise

    def insert_careers(self, db: Session):
        from src.core.models import career
        
        # Lee los datos del archivo JSON
        try:
            if db.query(career.Career).count() == 0:
                with open('src/core/data/career.json', 'r') as file:
                    career_data = json.load(file)
                    self.insert_data(db, career.Career, career_data['careers'])
        except FileNotFoundError:
            self.hyre.critical("El archivo career.json no fue encontrado.")
            raise
        except json.JSONDecodeError as e:
            self.hyre.critical(f"Error al decodificar el archivo JSON: {e}")
            raise

    def insert_roles(self, db: Session):
        from src.core.models import role
        
        # Lee los datos del archivo JSON
        try:
            if db.query(role.Role).count() == 0:
                with open('src/core/data/role.json', 'r') as file:
                    role_data = json.load(file)
                    self.insert_data(db, role.Role, role_data['roles'])
        except FileNotFoundError:
            self.hyre.critical("El archivo role.json no fue encontrado.")
            raise
        except json.JSONDecodeError as e:
            self.hyre.critical(f"Error al decodificar el archivo JSON: {e}")
            raise

    # Función para insertar datos en bloques
    def insert_data(self, db: Session, model, data: List[dict]):
        try:
            db.bulk_insert_mappings(model, data)  # Inserta los datos en bloques
            db.commit()  # Confirma la transacción
            self.hyre.success("Datos insertados correctamente.")
        except SQLAlchemyError as e:
            db.rollback()  # En caso de error, deshace la transacción
            self.hyre.critical(f"Database error occurred: {e}")
            raise
