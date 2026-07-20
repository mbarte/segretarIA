from functools import lru_cache

from app.services.llm import LLMService
from app.agents.assistant import AssistantAgent
from app.prompts.builder import PromptBuilder

from .config import settings
from app.providers.imap import IMAPProvider
from app.providers.graph import GraphEmailProvider
from app.providers.auth.microsoft import MicrosoftAuthenticator
from app.providers.auth.token_cache import TokenCache

from app.services.email import EmailService
from app.services.database import DatabaseService

from app.repositories.email import EmailRepository



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
def get_microsoft_authenticator(scopes: tuple):

    return MicrosoftAuthenticator(
        client_id=settings.azure_client_id,
        tenant_id=settings.azure_tenant_id,
        scopes=list(scopes),
        token_cache=TokenCache()
    )

@lru_cache
def get_email_provider():

    if settings.email_provider == "imap":

        return IMAPProvider(
            server=settings.imap_server,
            port=settings.imap_port,
            username=settings.email_address,
            authenticator=get_microsoft_authenticator(tuple(IMAPProvider.SCOPES)) #tuple because lru_cache needs hashable types
        )


    if settings.email_provider == "graph":

        return GraphEmailProvider(
            authenticator=get_microsoft_authenticator(tuple(GraphEmailProvider.SCOPES))
        )


    raise ValueError(
        "Unsupported email provider"
    )

@lru_cache
def get_database_service()-> DatabaseService:
    return DatabaseService()


@lru_cache
def get_email_repository() -> EmailRepository:
    return EmailRepository(
        database_service=get_database_service()
    )


@lru_cache
def get_email_service() -> EmailService:
    return EmailService(
        provider=get_email_provider(),
        repository=get_email_repository()
    )