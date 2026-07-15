from fastapi import APIRouter, Depends

from app.models.chat import ChatRequest
from app.core.dependencies import get_llm_service
from app.services.llm import LLMService

router = APIRouter(
    prefix = "/api/chat",
    tags = ["chat"]
)

@router.post("/")
async def chat(
    request: ChatRequest,
    llm: LLMService = Depends(get_llm_service)):

    response = await llm.chat(request.message)

    return {
        "response": response
    }