from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.schemas.alert import AlertResponse
from typing import List
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[AlertResponse])
def get_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alerts = db.query(Alert).filter(Alert.is_resolved==False).all()
    return alerts


@router.put("/{alert_id}/resolve", response_model=AlertResponse)
def update_status_of_alert(alert_id : int, db:Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    alert.is_resolved=True
    db.commit()
    db.refresh(alert)
    return alert

