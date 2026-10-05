from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class ChecklistStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"
    FAILED = "FAILED"

class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    visit_schedule_id = Column(Integer, ForeignKey("visit_schedules.id"), nullable=False)
    procedure_definition_id = Column(Integer, ForeignKey("procedure_definitions.id"), nullable=False)
    status = Column(Enum(ChecklistStatus), default=ChecklistStatus.PENDING)
    notes = Column(Text)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())