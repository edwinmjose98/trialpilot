from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.protocol import Protocol
from app.schemas.rag import AskRequest
from app.services import rag_service


router = APIRouter()

@router.post("/{protocol_id}/embed")
def embed_protocol_pdf(
        protocol_id: int,
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    protocol = db.query(Protocol).filter(Protocol.id == protocol_id).first()
    if not protocol:
        raise HTTPException(status_code=404, detail = "Protocol not found")
    
    pdf_bytes = file.file.read()
    count = rag_service.embed_protocol(protocol_id, pdf_bytes, db)
    return {"message": "Protocol embedded", "chunks_created": count}


@router.post("/{protocol_id}/ask")
def ask_protocol(
        protocol_id: int,
        request: AskRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    protocol = db.query(Protocol).filter(Protocol.id == protocol_id).first()
    if not protocol:
        raise HTTPException(status_code=404, detail = "Protocol not found")
    
    return rag_service.answer_question(protocol_id, request.question, db)
