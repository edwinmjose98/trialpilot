from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import User, Protocol, Patient, VisitDefinition, ProcedureDefinition, VisitSchedule, ChecklistItem
from app.api.v1 import protocols

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrialPilot",
    description="Clinical Trial Protocol Adherence System",
    version="0.1.0"
)

app.include_router(protocols.router, prefix = "/api/v1/protocols", tags = ["protocols"])

@app.get("/")
def health_check():
    return {"status": "ok", "app": "TrialPilot"}
