from fastapi import FastAPI
from app.routers import student
from app.db.database import Base, engine
from app.models.User import User
from app.routers import users
from app.routers import auth
from app.models import User, Attendance, emotion,attendance_report,motivation_report,report
from app.models.classe import Classe
from app.models.student import Student
# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion des étudiants")

# Inclusion des routes
app.include_router(student.router)

app.include_router(users.router)
app.include_router(auth.router)