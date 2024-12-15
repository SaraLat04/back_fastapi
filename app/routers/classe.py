from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.classe import ClasseCreate, ClasseResponse
from app.crud.classe import create_classe, update_classe, delete_classe, get_classe_by_id, get_all_classes
from app.models.classe import Classe
from typing import List

router = APIRouter(prefix="/classes", tags=["classes"])

@router.post("/", response_model=ClasseResponse)
def add_classe(classe: ClasseCreate, db: Session = Depends(get_db)):
    new_classe = create_classe(db, classe.nom, classe.id_teacher)
    return new_classe

@router.put("/{classe_id}", response_model=ClasseResponse)
def update_classe_route(classe_id: int, classe_data: ClasseCreate, db: Session = Depends(get_db)):
    db_classe = update_classe(db, classe_id, classe_data.nom, classe_data.id_teacher)
    if db_classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return db_classe

@router.delete("/{classe_id}", response_model=ClasseResponse)
def delete_classe_route(classe_id: int, db: Session = Depends(get_db)):
    db_classe = delete_classe(db, classe_id)
    if db_classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return db_classe

@router.get("/{classe_id}", response_model=ClasseResponse)
def get_classe_route(classe_id: int, db: Session = Depends(get_db)):
    db_classe = get_classe_by_id(db, classe_id)
    if db_classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return db_classe

@router.get("/", response_model=List[ClasseResponse])
def get_all_classes_route(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """
    Route pour récupérer une liste paginée de classes.
    """
    classes = get_all_classes(db, skip, limit)
    if not classes:
        raise HTTPException(status_code=404, detail="Aucune classe trouvée")
    return classes