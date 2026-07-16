from typing import List
from app.domain.email import Email
from app.providers.base import EmailProvider

class EmailService:

    def __init__(self, provider: EmailProvider):
        self.provider = provider

    def get_new_emails(self)-> List[Email]:
        
        emails = self.provider.fetch_unread()

        return emails