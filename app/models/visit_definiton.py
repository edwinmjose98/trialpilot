from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class VisitDefinition(Base):
    __tablename__ = "visit_definitions"

    id = Column(Integer, primary_key=True, index = True)
    protocol_id = Column(Integer, ForeignKey("protocols.id"), nullable=False)
    name = Column(String, nullable=False)
    day_number = Column(Integer)
    window_before = Column(Integer)
    window_after = Column(Integer)
    is_mandatory = Column(Boolean, default=True)
