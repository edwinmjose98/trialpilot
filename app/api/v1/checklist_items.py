from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.checklist_item import ChecklistItem
from app.schemas.checklist_item import ChecklistResponse
from typing import List
from datetime import datetime
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/{visit_schedule_id}/items", response_model=List[ChecklistResponse])
def get_alerts(visit_schedule_id : int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    checklistItems = db.query(ChecklistItem).filter(ChecklistItem.visit_schedule_id==visit_schedule_id).all()
    return checklistItems


@router.put("/{checklist_item_id}/resolve", response_model=ChecklistResponse)
def update_status_of_alert(checklist_item_id : int, db:Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    checklistItem = db.query(ChecklistItem).filter(ChecklistItem.id == checklist_item_id).first()
    checklistItem.status="COMPLETED"
    checklistItem.completed_at = datetime.now()
    db.commit()
    db.refresh(checklistItem)
    return checklistItem

