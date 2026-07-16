from abc import ABC, abstractmethod

class AuthenticationProvider(ABC):

    @abstractmethod
    def get_access_token(self) -> str:
        """Restituisce un access token valido."""
        raise NotImplementedError