import ollama 
from app.core.config import settings

class LLMService:

    def __init__(self):
        self.client = ollama.Client(
            host = settings.ollama_host
        )
    
    async def chat(self, message:str)-> str: #ollama fa una chiamata HTTP sincrona, predisposizione futura (TODO)
        response = self.client.chat(
            model = settings.ollama_model,
            messages = [
                {
                    "role": "user",
                    "content": message
                }
            ],
            keep_alive = settings.ollama_keep_alive
        )

        return response["message"]["content"]