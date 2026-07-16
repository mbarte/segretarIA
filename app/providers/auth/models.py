from dataclasses import dataclass
from datetime import datetime

@dataclass
class OAuthToken:
    access_token: str
    refresh_token: str
    expires_at: datetime

    @property
    def expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at