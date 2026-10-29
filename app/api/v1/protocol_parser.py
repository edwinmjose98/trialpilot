import fitz  # PyMuPDF
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.protocol import Protocol
from app.services import protocol_parser
import io

router = APIRouter()

@router.post("/{protocol_id}/parse-pdf")
def parse_protocol_pdf(
    protocol_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    protocol = db.query(Protocol).filter(Protocol.id == protocol_id).first()
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    
    pdf_bytes = file.file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    
    parsed_data = protocol_parser.parse_protocol_text(text)
    protocol_parser.save_parsed_protocol(protocol_id, parsed_data, db)
    
    return {"message": "Protocol parsed successfully", "visits_created": len(parsed_data["visit_definitions"])}