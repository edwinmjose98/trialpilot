from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import User, Protocol, Patient, VisitDefinition, ProcedureDefinition, VisitSchedule, ChecklistItem, Alert
from app.api.v1 import protocols
from app.api.v1 import patients
from app.api.v1 import visit_definitions
from app.api.v1 import alerts
from app.api.v1 import procedure_definitions
from app.api.v1 import checklist_items
from app.api.v1 import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrialPilot",
    description="Clinical Trial Protocol Adherence System",
    version="0.1.0"
)

app.include_router(protocols.router, prefix = "/api/v1/protocols", tags = ["protocols"])
app.include_router(patients.router, prefix = "/api/v1/patients", tags = ["patients"])
app.include_router(visit_definitions.router, prefix = "/api/v1/visitdefinitions", tags = ["visit definitions"])
app.include_router(alerts.router, prefix = "/api/v1/alerts", tags=["alerts"])
app.include_router(procedure_definitions.router, prefix = "/api/v1/procedure_definitions", tags=["procedure definitions"])
app.include_router(checklist_items.router, prefix = "/api/v1/checklist_items", tags=["checklist items"])
app.include_router(auth.router, prefix = "/api/v1/auth", tags=["authorization"])

@app.get("/")
def health_check():
    return {"status": "ok", "app": "TrialPilot"}
