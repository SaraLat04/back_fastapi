from sqlalchemy.orm import Session
from app.models.classe import Classe
from datetime import datetime
from typing import Optional

def get_classe_by_id(db: Session, classe_id: int):
    """Récupérer une classe par ID."""
    return db.query(Classe).filter(Classe.id == classe_id).first()

def get_all_classes(db: Session, skip: int = 0, limit: int = 10):
    """Récupérer une liste de classes avec pagination."""
    return db.query(Classe).offset(skip).limit(limit).all()

def create_classe(db: Session, nom: str, id_teacher: int):
    """Créer une nouvelle classe."""
    db_classe = Classe(
        nom=nom,
        id_teacher=id_teacher,
    )
    db.add(db_classe)
    db.commit()
    db.refresh(db_classe)
    return db_classe

def update_classe(db: Session, classe_id: int, nom: Optional[str] = None, id_teacher: Optional[int] = None):
    """Mettre à jour les informations d'une classe."""
    db_classe = get_classe_by_id(db, classe_id)
    if db_classe:
        if nom:
            db_classe.nom = nom
        if id_teacher:
            db_classe.id_teacher = id_teacher
        db.commit()
        db.refresh(db_classe)
    return db_classe

def delete_classe(db: Session, classe_id: int):
    """Supprimer une classe."""
    db_classe = get_classe_by_id(db, classe_id)
    if db_classe:
        db.delete(db_classe)
        db.commit()
    return db_classe