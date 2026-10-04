from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class PatientStatus(enum.Enum):
    SCREENING = "SCREENING"
    ENROLLED = "ENROLLED"
    ACTIVE = "ACTIVE" 
    COMPLETED = "COMPLETED"
    WITHDRAWN = "WITHDRAWN"
    SCREEN_FAILED = "SCREEN_FAILED"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key = True, index = True)
    mrn = Column(String, nullable = False, unique = True)
    full_name = Column(String, nullable = False)
    date_of_birth = Column(Date)
    gender = Column(String)
    email = Column(String)
    phone = Column(String)
    status = Column(Enum(PatientStatus), default = PatientStatus.SCREENING)
    enrollment_date = Column(Date)
    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

