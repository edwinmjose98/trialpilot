from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class AlertType(enum.Enum):
    VISIT_OVERDUE = "VISIT_OVERDUE"
    WINDOW_CLOSING = "WINDOW_CLOSING"
    MISSED_PROCEDURE = "MISSED_PROCEDURE"
    DOSE_BLOCKED = "DOSE_BLOCKED"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index = True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    visit_schedule_id = Column(Integer, ForeignKey("visit_schedules.id"), nullable=False)
    alert_type = Column(Enum(AlertType))
    message = Column(String)
    is_resolved = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())