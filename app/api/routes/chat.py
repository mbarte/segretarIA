from fastapi import APIRouter, Depends

from app.models.chat import ChatRequest
from app.models.agent import AgentRequest
from app.core.dependencies import get_assistant_agent
from app.agents.assistant import AssistantAgent

router = APIRouter(
    prefix = "/api/chat",
    tags = ["chat"]
)

@router.post("")
async def chat(
    request: ChatRequest,
    assistant: AssistantAgent = Depends(get_assistant_agent)):

    agent_request = AgentRequest(message = request.message)
    response = await assistant.run(agent_request)

    return response