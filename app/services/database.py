from sqlalchemy.orm import Session

from app.database.engine import SessionLocal
from app.database.models import Conversation

class DatabaseService:

    def get_session(self)-> Session:
        return SessionLocal()


    def save_message(
        self,
        role: str,
        content: str
    ):

        session = self.get_session()

        try:

            message = Conversation(
                role=role,
                content=content
            )

            session.add(message)

            session.commit()

        finally:

            session.close()