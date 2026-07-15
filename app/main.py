from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.database.engine import Base, engine
from app.database import models

def create_app() -> FastAPI:

    setup_logging()
    
    Base.metadata.create_all(
        bind=engine
    ) #controlla il db e crea tabelle inesistenti

    app = FastAPI(
        title = settings.app_name,
        version = settings.app_version
    )

    app.include_router(api_router)
    

    @app.get("/")
    async def root():
        return {
            "message": "segretarIA is running"
        }

    @app.get("/api/health")
    async def health():
        
        return {
            "status": "ok",
            "version": settings.app_version,
            "model": settings.ollama_model
        }
    
    return app

app = create_app()