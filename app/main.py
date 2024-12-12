from fastapi import FastAPI
from app.routers import student
from app.db.database import Base, engine

# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion des étudiants")

# Inclusion des routes
app.include_router(student.router)
