from pydantic import BaseModel

class ProcedureDefinitionCreate(BaseModel):
    visit_definition_id: int
    name: str
    procedure_type: str
    is_mandatory: bool

class ProcedureDefinitionResponse(ProcedureDefinitionCreate):
    id: int

    class Config:
        from_attributes = True