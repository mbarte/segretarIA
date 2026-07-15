from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class Task:

    description: str

    priority: str

    due_date: date | None

    source_email_uid: int | None