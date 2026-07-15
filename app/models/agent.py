# "contratto" tra API e Agent
from pydantic import BaseModel

class AgentRequest(BaseModel):

    message: str

    session_id: str | None = None

class AgentResponse(BaseModel):

    answer: str