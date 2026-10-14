from pydantic import BaseModel
from datetime import datetime

class ProtocolCreate(BaseModel):
    title : str
    protocol_number : str
    version : str
    sponsor : str
    phase : str
    indication : str
    description : str

class ProtocolResponse(ProtocolCreate):
    id : int
    status : str
    created_at : datetime

    class Config:
        from_attributes = True
