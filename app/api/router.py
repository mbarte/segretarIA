from fastapi import APIRouter
from app.api.routes import chat, email


api_router = APIRouter()


api_router.include_router(
    chat.router
)

api_router.include_router(
    email.router
)