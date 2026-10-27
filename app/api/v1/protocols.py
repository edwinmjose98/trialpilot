from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.protocol import ProtocolCreate, ProtocolResponse
from app.models.protocol import Protocol
from app.models.alert import Alert
from typing import List
from app.services import alert_service
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ProtocolResponse)
def create_protocol(protocol: ProtocolCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_protocol = Protocol(**protocol.model_dump())
    db.add(db_protocol)
    db.commit()
    db.refresh(db_protocol)
    return db_protocol

@router.get("/", response_model=List[ProtocolResponse])
def get_protocols(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    protocols = db.query(Protocol).all()
    return protocols

@router.get("/{protocol_id}", response_model=ProtocolResponse)
def get_protocol(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    protocol = db.query(Protocol).filter(Protocol.id == id).first()
    return protocol

@router.post("/check-alerts")
def trigger_alert_check(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert_service.check_and_create_alert(db)
    return {"message": "Alert check completed"}

