from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, update_user, delete_user, get_user_by_id, get_all_users
from app.models.User import User  
from typing import List  # Importation correcte de List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")
    new_user = create_user(db, user)
    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user_data)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user


@router.get("/", response_model=List[UserResponse])
def get_all_users_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """
    Route pour récupérer une liste paginée d'utilisateurs.
    """
    users = get_all_users(db, skip, limit)
    if not users:
        raise HTTPException(status_code=404, detail="Aucun utilisateur trouvé")
    return users


@router.get("/role", response_model=List[UserResponse])
def get_users_by_role_route(role: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """
    Route pour récupérer une liste paginée d'utilisateurs filtrée par rôle.
    """
    users = db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail=f"Aucun utilisateur avec le rôle {role} trouvé")
    return users

@router.get("/teachers", response_model=List[UserResponse])
def get_teachers(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    teachers = db.query(User).filter(User.role == 'teacher').offset(skip).limit(limit).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="Aucun enseignant trouvé.")
    return teachers

@router.get("/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user



