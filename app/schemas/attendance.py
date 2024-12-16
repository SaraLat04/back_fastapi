from pydantic import BaseModel
from enum import Enum

class AttendanceStatus(str, Enum):
    present = 'present'
    absent = 'absent'

class Attendance(BaseModel):
    id: int
    student_id: int
    class_id: int
    date: str
    status: AttendanceStatus