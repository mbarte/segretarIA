from  abc import ABC, abstractmethod
from typing import List
from app.domain.email import Email

class EmailProvider(ABC):
    
    @abstractmethod
    def fetch_unread(self)-> List[Email]:
        pass