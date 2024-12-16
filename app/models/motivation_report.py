from sqlalchemy import Column, Integer, Float, String
from app.db.database import Base

class MotivationReport(Base):
    __tablename__ = "motivation_reports"
    
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    average_motivation_score = Column(Float, nullable=False)
    mood_analysis = Column(String, nullable=False)
