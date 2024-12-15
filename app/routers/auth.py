from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.database import get_db
from app.utils.jwt import create_access_token
from app.schemas.user import UserAuth
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.crud.user import get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Auth"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login")
def login(form_data: UserAuth, db: Session = Depends(get_db)):
    # Récupérer l'utilisateur en fonction de l'email
    user = get_user_by_username(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Générer le token d'accès
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Retourner le token et le rôle de l'utilisateur
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role.value  # Assurez-vous que role est de type Enum
    }