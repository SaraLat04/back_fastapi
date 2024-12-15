from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClasseResponse(BaseModel):
    id: int
    date: datetime
    nom: str
    id_teacher: int

    class Config:
        from_attributes = True  # Permet de traiter les objets ORM directement

class ClasseCreate(BaseModel):
    nom: str
    id_teacher: int