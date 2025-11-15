from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import get_settings
from .database import Base, engine
from .routers import catalog, employees

# Create tables for demo purposes (real deployments should rely on Alembic migrations).
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(title="NeedAnalyze API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(catalog.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
