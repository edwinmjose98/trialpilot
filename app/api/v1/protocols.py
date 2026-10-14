from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.protocol import ProtocolCreate, ProtocolResponse
from app.models.protocol import Protocol
from typing import List

router = APIRouter()

@router.post("/", response_model=ProtocolResponse)
def create_protocol(protocol: ProtocolCreate, db: Session = Depends(get_db)):
    db_protocol = Protocol(**protocol.model_dump())
    db.add(db_protocol)
    db.commit()
    db.refresh(db_protocol)
    return db_protocol

@router.get("/", response_model=List[ProtocolResponse])
def get_protocol(db: Session = Depends(get_db)):
    protocols = db.query(Protocol).all()
    return protocols

@router.get("/{protocol_id}", response_model=ProtocolResponse)
def get_protocol(id: int, db: Session = Depends(get_db)):
    protocol = db.query(Protocol).filter(Protocol.id == id).first()
    return protocol


