from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class Classe(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    nom = Column(String, nullable=False)
    id_teacher = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relation avec User, filtrée pour le rôle teacher
    user = relationship("User", back_populates="classes")