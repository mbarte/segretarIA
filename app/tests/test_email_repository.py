from datetime import datetime

from app.domain.email import Email
from app.repositories.email import EmailRepository
from app.services.database import DatabaseService
from app.database.engine import Base, engine


Base.metadata.create_all(bind=engine)


def test_save_and_load_email():

    repository = EmailRepository(DatabaseService())

    email = Email(
        uid="123",
        message_id="test-message-id",
        subject="Repository Test",
        sender="mario@test.it",
        recipients=["luigi@test.it"],
        date=datetime.now(),
        body="Questa è una email di test.",
        is_read=False,
        has_attachments=False,
        attachments=[]
    )

    repository.save(email)

    loaded = repository.get("test-message-id")

    assert loaded is not None
    assert loaded.message_id == email.message_id
    assert loaded.subject == email.subject
    assert loaded.sender == email.sender
    assert loaded.body == email.body
    assert loaded.recipients == email.recipients
    assert loaded.has_attachments is False


def test_exists():

    repository = EmailRepository(DatabaseService())

    assert repository.exists("test-message-id")
    assert not repository.exists("non-existing-id")


def test_save_many_emails():

    repository = EmailRepository(DatabaseService())

    emails = [
        Email(
            uid="1",
            message_id="batch-1",
            subject="Test 1",
            sender="sender@test.com",
            recipients=["receiver@test.com"],
            date=datetime.now(),
            body="Email 1",
            is_read=False,
            has_attachments=False,
            attachments=[]
        ),
        Email(
            uid="2",
            message_id="batch-2",
            subject="Test 2",
            sender="sender@test.com",
            recipients=["receiver@test.com"],
            date=datetime.now(),
            body="Email 2",
            is_read=False,
            has_attachments=False,
            attachments=[]
        )
    ]

    repository.save_many(emails)

    assert repository.exists("batch-1")
    assert repository.exists("batch-2")

test_save_and_load_email()
test_exists()
test_save_many_emails()