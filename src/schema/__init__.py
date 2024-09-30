from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from typing import Dict

class UserRepository(ABC):
    """
    User repository interface
    """
    
    #Inicio de Sesión
    @abstractmethod
    def login(self, request:dict, db: Session):
        pass
    
    @abstractmethod
    def refresh_token(self, access_token: str, db: Session, is_get: bool = True, refresh_token: str = '', expires_at: int = 0):
        pass
    
    @abstractmethod
    def logout(self, access_token: str, db: Session):
        pass
    
    @abstractmethod
    def logout_others(self, access_token: str, db: Session):
        pass
    
    @abstractmethod
    def get_all(self, db: Session):
        pass

    @abstractmethod
    def get(self, id: str, db: Session):
        pass

    @abstractmethod
    def create(self, request: Dict, db: Session, background_tasks: BackgroundTasks):
        pass

    @abstractmethod
    def update(self, id: str, request: Dict, db: Session, background_tasks: BackgroundTasks):
        pass