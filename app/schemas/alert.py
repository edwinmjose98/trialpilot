from pydantic import BaseModel
from datetime import datetime
class AlertResponse(BaseModel):
    id : int
    patient_id : int
    visit_schedule_id : int
    alert_type : str
    message : str
    is_resolved : bool
    created_at : datetime

    class Config:
        from_attributes = True