from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
from enum import Enum as PyEnum

# Définir l'énumération des rôles
class RoleEnum(PyEnum):
    teacher = "teacher"
    admin = "admin"
    etudiant = "etudiant"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # Le bon champ
    is_active = Column(Boolean, default=True)
    role = Column(Enum(RoleEnum), nullable=False)  # Enum pour le rôle