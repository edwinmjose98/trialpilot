from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import User, Protocol

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TrialPilot",
    description="Clinical Trial Protocol Adherence System",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "ok", "app": "TrialPilot"}
