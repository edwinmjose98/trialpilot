from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.visit_definition import VisitDefinitionCreate, VisitDefinitionResponse
from app.models.visit_definiton import VisitDefinition

router = APIRouter()


@router.post("/", response_model=VisitDefinitionResponse)
def create_visit_defintion(visit_definition: VisitDefinitionCreate, db : Session = Depends(get_db)):
    db_visit_defintion=VisitDefinition(**visit_definition.model_dump())
    db.add(db_visit_defintion)
    db.commit()
    db.refresh(db_visit_defintion)
    return db_visit_defintion