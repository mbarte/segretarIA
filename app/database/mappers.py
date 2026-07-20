# Domain <-> Model mapping
import json

from app.domain.email import Email, EmailAttachment
from app.database.models import EmailModel, AttachmentModel

def email_to_model(email: Email) -> EmailModel:
    """
    Converts an Email object in the corresponding SQLAlchemy model
    """
    attachments = [
        AttachmentModel(
            filename = attachment.filename,
            content_type = attachment.content_type,
            size = attachment.size
        )
        for attachment in email.attachments
    ]

    return EmailModel(
        uid=email.uid,
        message_id=email.message_id,
        subject=email.subject,
        sender=email.sender,
        recipients=json.dumps(email.recipients),
        date=email.date,
        body=email.body,
        is_read=email.is_read,
        has_attachments=email.has_attachments,
        attachments=attachments
    )


    


def model_to_email(model: EmailModel) -> Email:
    """
    Converts a SQLAlchemy object in the corresponding Email model
    """
    attachments = [
        EmailAttachment(
            filename = attachment.filename,
            content_type = attachment.content_type,
            size = attachment.size
        )
        for attachment in model.attachments
    ]

    return Email(
        uid=model.uid,
        message_id=model.message_id,
        subject=model.subject,
        sender=model.sender,
        recipients=json.loads(model.recipients),
        date=model.date,
        body=model.body,
        is_read=model.is_read,
        has_attachments=model.has_attachments,
        attachments=attachments,
    )