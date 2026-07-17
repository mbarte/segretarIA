from dataclass import dataclass

from typing import List
from app.domain.email import Email
from app.providers.base import EmailProvider
from app.repositories.email import EmailRepository

@dataclass
class EmailSyncResult:
    fetched: int
    saved: int
    skipped: int 
    errors: int
    

class EmailService:

    def __init__(self, provider: EmailProvider, repository: EmailRepository):
        self.provider = provider
        self.repository = repository

    def initialize(self) -> EmailSyncResult:

        since = datetime.now() - timedelta(
                days=self.settings.email_initial_sync_months * 30
            )

        emails = self.provider.fetch_since(since)

        return self._save_emails(emails)

    def sync(self)-> EmailSyncResult:
        
        emails: List[Emails] = self.provider.fetch_unread()

        return self._save_emails(emails)
    
    def _save_emails(self, emails: List[Email]) -> EmailSyncResult:

        saved = 0
        skipped = 0
        errors = 0

        for email in emails:
            try:
                if self.repository.exists(email.message_id):
                    skipped +=1
                    continue

                self.repository.save(email)
                saved += 1

            except Exception:
                errors += 1
        
        return EmailSyncResult(
            fetched=len(emails),
            saved=saved,
            skipped=skipped,
            errors=errors
        )