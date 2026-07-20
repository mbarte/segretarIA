from dataclasses import dataclass
from datetime import datetime, timedelta

from typing import List
import logging
logger = logging.getLogger(__name__) 

from app.core.config import settings
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
                days=settings.email_initial_sync_months * 30
            )

        emails = self.provider.fetch_since(since)
        
        logger.info("Avvio inizializzazione mailbox")
        result = self._save_emails(emails)
        logger.info(
            "Inizializzazione completata: fetched=%d, saved=%d, skipped=%d, errors=%d",
            result.fetched, result.saved, result.skipped, result.errors
        )
        return result


    def sync(self)-> EmailSyncResult:
        
        emails: List[Email] = self.provider.fetch_unread()

        logger.info("Avvio sync incrementale")
        result = self._save_emails(emails)
        logger.info(
            "Sync completata: fetched=%d, saved=%d, skipped=%d, errors=%d",
            result.fetched, result.saved, result.skipped, result.errors
        )
        return result
    
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