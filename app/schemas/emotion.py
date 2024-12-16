from pydantic import BaseModel

class Emotion(BaseModel):
    id: int
    student_id: int
    class_id: int 
    date: str
    emotion: str
    confidence: float