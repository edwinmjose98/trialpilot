from pydantic import BaseModel
class VisitDefinitionCreate(BaseModel):
    protocol_id : int
    name : str
    day_number : int
    window_before : int
    window_after : int
    is_mandatory : bool


class VisitDefinitionResponse(VisitDefinitionCreate):
    id : int

    class Config:
        from_attributes = True