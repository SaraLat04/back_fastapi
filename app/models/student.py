from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from app.db.database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    photo_path = Column(String, nullable=True)  # Path to the uploaded photo
    face_encoding = Column(LargeBinary, nullable=True)  # Encoded face
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    classroom = relationship("Classe", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")
    emotions = relationship("Emotion", back_populates="student")