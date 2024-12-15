from sqlalchemy.orm import Session
from app.models.User import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from typing import Optional


def get_user_by_id(db: Session, user_id: int):
    """Récupérer un utilisateur par ID."""
    return db.query(User).filter(User.id == user_id).first()



def get_user_by_username(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    """Récupérer une liste d'utilisateurs avec pagination."""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """Créer un nouvel utilisateur."""
    hashed_password = hash_password(user.password)  # Utilisez hash_password ici
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,  # Utilisez hashed_password ici
        role=user.role,
        is_active=True,  # Par défaut, actif
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def update_user(db: Session, user_id: int, user_data: UserCreate):
    """Mettre à jour les informations d'un utilisateur."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.username = user_data.username
        db_user.email = user_data.email
        db_user.hashed_password = hash_password(user_data.password)  # Utilisez hashed_password ici
        db_user.role = user_data.role
        db.commit()
        db.refresh(db_user)
    return db_user



def delete_user(db: Session, user_id: int):
    """Supprimer un utilisateur."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user