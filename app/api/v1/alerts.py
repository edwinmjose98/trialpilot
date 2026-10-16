from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.schemas.alert import AlertResponse
from typing import List

router = APIRouter()


@router.get("/", response_model=List[AlertResponse])
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.is_resolved==False).all()
    return alerts


@router.put("/{alert_id}/resolve", response_model=AlertResponse)
def update_status_of_alert(alert_id : int, db:Session=Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    alert.is_resolved=True
    db.commit()
    db.refresh(alert)
    return alert

