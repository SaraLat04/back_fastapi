from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    generated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_generated = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
