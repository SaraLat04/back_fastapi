from pydantic import BaseModel

class MotivationReport(BaseModel):
    id: int
    average_motivation_score: float
    mood_analysis: str