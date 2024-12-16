from pydantic import BaseModel

class Report(BaseModel):
    id: int 
    class_id: int
    generated_by: int
    date_generated: str
    file_path: str