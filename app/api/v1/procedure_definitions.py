from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.procedure_definition import ProcedureDefinitionCreate, ProcedureDefinitionResponse
from app.models.procedure_definition import ProcedureDefinition

router = APIRouter()

@router.post("/", response_model=ProcedureDefinitionResponse)
def create_procedure_definition(procedure_definition: ProcedureDefinitionCreate, db : Session = Depends(get_db)):
    db_procedure_definition = ProcedureDefinition(**procedure_definition.model_dump())
    db.add(db_procedure_definition)
    db.commit()
    db.refresh(db_procedure_definition)
    return db_procedure_definition