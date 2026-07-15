from app.prompts.system import SYSTEM_PROMPT
from app.models.agent import AgentRequest

class PromptBuilder:

    def build(self, request:AgentRequest)-> list[dict]:
        #ollama si aspetta una lista di messaggi
        return [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content": request.message
            }
        ]