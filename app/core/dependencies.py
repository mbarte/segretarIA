from app.services.llm import LLMService

_llm_service = None

def get_llm_service() -> LLMService:

    global _llm_service

    if _llm_service is None:
        _llm_service = LLMService()
    
    return _llm_service