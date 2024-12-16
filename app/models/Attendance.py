from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class AttendanceStatus(enum.Enum):
    present = "present"
    absent = "absent"

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    date = Column(String, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)

    student = relationship("Student", back_populates="attendances")
    classroom = relationship("Classe", back_populates="attendances")
