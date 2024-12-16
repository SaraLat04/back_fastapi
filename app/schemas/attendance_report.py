from pydantic import BaseModel

class AttendanceReport(BaseModel):
    id: int
    total_absences: int
    total_present: int