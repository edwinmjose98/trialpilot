from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class ProtocolStatus(enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    SUSPENDED = "SUSPENDED"

class Protocol(Base):
    __tablename__ = "protocols"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    protocol_number = Column(String, unique=True, nullable=False)
    version = Column(String, nullable=False)
    sponsor = Column(String)
    status = Column(Enum(ProtocolStatus), default=ProtocolStatus.DRAFT)
    phase = Column(String)  # Phase I, II, III, IV
    indication = Column(String)  # e.g. "Breast Cancer"
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())