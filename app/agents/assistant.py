from app.services.llm import LLMService
from app.models.agent import (AgentRequest, AgentResponse)
from app.prompts.builder import PromptBuilder


class AssistantAgent:

    def __init__(self, 
        llm: LLMService,
        prompt_builder: PromptBuilder
    ):
        self._llm = llm
        self._prompt_builder =  prompt_builder

    async def run(self, request: AgentRequest) -> AgentResponse:

        messages = self._prompt_builder.build(request)

        answer = await self._llm.chat(messages)

        return AgentResponse(
            answer=answer
        )
