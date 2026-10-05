from sqlalchemy import Column, Integer, Date, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class VisitStatus(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"
    OVERDUE = "OVERDUE"

class VisitSchedule(Base):
    __tablename__ = "visit_schedules"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_definition_id = Column(Integer, ForeignKey("visit_definitions.id"), nullable=False)
    scheduled_date = Column(Date)
    actual_date = Column(Date)
    status = Column(Enum(VisitStatus), default=VisitStatus.SCHEDULED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())