import ollama 
from app.core.config import settings

class LLMService:

    def __init__(self):
        self.client = ollama.Client(
            host = settings.ollama_host
        )
    
    async def chat(self, messages:list[dict])-> str: #ollama fa una chiamata HTTP sincrona, async predisposizione futura 
        response = self.client.chat(
            model = settings.ollama_model,
            messages = messages,
            keep_alive = settings.ollama_keep_alive
        )

        return response["message"]["content"]