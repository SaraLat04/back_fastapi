from sqlalchemy import Column, Integer
from app.db.database import Base

class AttendanceReport(Base):
    __tablename__ = "attendance_reports"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    total_absences = Column(Integer, nullable=False)
    total_present = Column(Integer, nullable=False)

