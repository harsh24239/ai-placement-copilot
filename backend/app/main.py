from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.upload import router as upload_router

app = FastAPI(title="AI Placement Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is alive"}