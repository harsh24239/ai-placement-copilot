from fastapi import FastAPI

app = FastAPI(title="AI Placement Copilot")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is alive"}