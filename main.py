from fastapi import FastAPI

app = FastAPI(
    title="TrialPilot",
    description="Clinical Trial Protocol Adherence System",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "ok", "app": "TrialPilot"}
