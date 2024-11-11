from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.core.connection import Base

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rating_value = Column(Integer, nullable=False)  # Valor del rating, por ejemplo de 1 a 5
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Relación con el usuario
    user = relationship("User", foreign_keys=[user_id])  # Relación con el usuario
    
    publication_id = Column(Integer, ForeignKey('publications.id'), nullable=False)  # Relación con la publicación
    publication = relationship("Publication", foreign_keys=[publication_id])  # Relación con la publicación