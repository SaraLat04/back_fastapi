from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    photo_url: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True
