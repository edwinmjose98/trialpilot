from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.visit_definition import VisitDefinitionCreate, VisitDefinitionResponse
from app.models.visit_definiton import VisitDefinition
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=VisitDefinitionResponse)
def create_visit_defintion(visit_definition: VisitDefinitionCreate, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_visit_defintion=VisitDefinition(**visit_definition.model_dump())
    db.add(db_visit_defintion)
    db.commit()
    db.refresh(db_visit_defintion)
    return db_visit_defintion