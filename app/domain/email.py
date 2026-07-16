from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class EmailAttachment:
    filename: str
    content_type: str
    size: int

@dataclass(slots=True)
class Email:

    uid: str | None
    message_id: str

    subject: str
    sender: str

    recipients: List[str]

    date: datetime

    body: str

    is_read: bool

    has_attachments: bool

    attachments: List[EmailAttachment]