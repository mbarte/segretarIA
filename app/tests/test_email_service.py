from datetime import datetime

from app.domain.email import Email
from app.repositories.email import EmailRepository
from app.services.database import DatabaseService
from app.services.email import EmailService


class FakeEmailProvider:


    def fetch_since(self, limit: int):

        return [
            Email(
                uid="1",
                message_id="init-1",
                subject="Prima email",
                sender="sender@test.com",
                recipients=["me@test.com"],
                date=datetime.now(),
                body="Email iniziale",
                is_read=False,
                has_attachments=False,
                attachments=[]
            )
        ]


    def fetch_unread(self):

        return [
            Email(
                uid="2",
                message_id="sync-1",
                subject="Nuova email",
                sender="sender@test.com",
                recipients=["me@test.com"],
                date=datetime.now(),
                body="Nuova email ricevuta",
                is_read=False,
                has_attachments=False,
                attachments=[]
            )
        ]



def test_initialize():

    service = EmailService(
        provider=FakeEmailProvider(),
        repository=EmailRepository(DatabaseService())
    )


    result = service.initialize()


    assert result.fetched == 1
    assert result.saved == 1
    assert result.errors == 0



def test_sync():

    service = EmailService(
        provider=FakeEmailProvider(),
        repository=EmailRepository(DatabaseService())
    )


    result = service.sync()


    assert result.fetched == 1
    assert result.saved == 1
    assert result.errors == 0


if __name__ == "__main__":

    test_initialize()
    test_sync()

    print("All tests passed")