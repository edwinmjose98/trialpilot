from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class ChecklistResponse(BaseModel):
    id : int
    visit_schedule_id : int
    procedure_definition_id : int
    status : str
    notes : Optional[str] = None
    completed_at : Optional[datetime] = None
    created_at : datetime

    class Config:
        from_attributes = True