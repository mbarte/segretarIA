from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Email:

    uid: int

    subject: str

    sender: str

    recipients: list[str]

    date: datetime

    body: str

    is_read: bool

    has_attachments: bool