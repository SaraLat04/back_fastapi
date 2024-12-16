from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Classe(Base):
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    teacher = relationship("User", back_populates="classes")
    emotions = relationship("Emotion", back_populates="classroom")
    attendances = relationship("Attendance", back_populates="classroom")
    students = relationship("Student", back_populates="classroom") 