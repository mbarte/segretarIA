from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    curl \
    -X POST http://localhost:5000/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message":"..."}'
    """
    message: str