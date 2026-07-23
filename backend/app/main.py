from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.upload import router as upload_router
from app.auth_routes import router as auth_router
from database.init_db import init_db

app = FastAPI(title="AI Placement Copilot")

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5180", "http://127.0.0.1:5180"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend is alive"}
