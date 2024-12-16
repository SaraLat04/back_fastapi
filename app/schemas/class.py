from pydantic import BaseModel

class Classe(BaseModel):
    id: int
    name: str
    teacher_id: int
