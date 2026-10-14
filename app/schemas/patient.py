from pydantic import BaseModel
from datetime import date, datetime
class PatientCreate(BaseModel):
    mrn : str
    full_name : str
    date_of_birth : date
    gender : str
    email : str
    phone : str
    enrollment_date: datetime
    protocol_id : int

class PatientResponse(PatientCreate):
    id : int
    status : str
    created_at : datetime

    class Config:
        from_attributes = True