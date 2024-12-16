from pydantic import BaseModel

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    class_id: int
    photo_path: str | None = None
    face_encoding: bytes | None = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True