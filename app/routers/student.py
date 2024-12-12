from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.student import Student, StudentCreate
from app.crud.student import get_students, get_student_by_id, create_student, update_student, delete_student

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=list[Student])
def read_students(db: Session = Depends(get_db)):
    return get_students(db)

@router.get("/{student_id}", response_model=Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return student

@router.post("/", response_model=Student)
def add_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, student)

@router.put("/{student_id}", response_model=Student)
def modify_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    updated_student = update_student(db, student_id, student.dict())
    if not updated_student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return updated_student

@router.delete("/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db)):
    deleted_student = delete_student(db, student_id)
    if not deleted_student:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return {"message": "Étudiant supprimé"}
