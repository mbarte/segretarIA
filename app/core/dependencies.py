from functools import lru_cache

from app.services.llm import LLMService
from app.agents.assistant import AssistantAgent
from app.prompts.builder import PromptBuilder


@lru_cache #sostituisce global _llm_service if _llm_service is None
def get_llm_service() -> LLMService:
    return LLMService()

@lru_cache
def get_prompt_builder() -> PromptBuilder:
    return PromptBuilder()

@lru_cache
def get_assistant_agent() -> AssistantAgent:
    
    return AssistantAgent(
        llm = get_llm_service(),
        prompt_builder= get_prompt_builder()
    )

@lru_cache
def get_email_provider():

    if settings.email_provider == "imap":
        return IMAPProvider(
            server=settings.imap_server,
            port=settings.imap_port,
            username=settings.email_username,
            password=settings.email_password
        )
    
    raise ValueError(
        "Unsupported email provider"
    )