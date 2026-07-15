from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes.chat import router as chat_router

def create_app() -> FastAPI:

    setup_logging()

    app = FastAPI(
        title = settings.app_name,
        version = settings.app_version
    )

    app.include_router(chat_router)

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