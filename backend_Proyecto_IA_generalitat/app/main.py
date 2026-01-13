from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.api.v1.router import router as v1_router

# Register models with SQLAlchemy
from app.models.user import User  # noqa: F401
from app.models.chat import Chat  # noqa: F401
from app.models.message import Message  # noqa: F401


app = FastAPI(title="Aula Virtual - IA Entrevistador", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
