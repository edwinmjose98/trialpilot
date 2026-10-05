from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class ProcedureDefinition(Base):
    __tablename__ = "procedure_definitions"

    id = Column(Integer, primary_key=True, index = True)
    visit_definition_id = Column(Integer, ForeignKey("visit_definitions.id"), nullable = False)
    name = Column(String, nullable = False)
    procedure_type = Column(String)
    is_mandatory = Column(Boolean, default=True)
