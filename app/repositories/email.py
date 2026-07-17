from app.database.mappers import email_to_model, model_to_email
from app.database.models import EmailModel
from app.domain.email import Email
from app.services.database import DatabaseService

class EmailRepository():

    def __init__(self, database_service: DatabaseService):
        self.database = database_service


    def save(self, email: Email) -> None:

        session = self.database.get_session()

        try:

            model = email_to_model(email)

            session.add(model)

            session.commit()

        finally:

            session.close()


    def save_many(self, emails: list[Email]) -> None:

        session = self.database.get_session()

        try:

            models = [
                email_to_model(email)
                for email in emails
            ]

            session.add_all(models)

            session.commit()

        finally:

            session.close()

    
    def exists(self, message_id: str) -> bool:

        session = self.database.get_session()
        try:
            return (
                session.query(EmailModel)
                .filter_by(message_id=message_id)
                .first()
                is not None
            )
        finally:
            session.close()


    def get(self, message_id: str) -> Email | None:

        session = self.database.get_session()

        try:
            model = (
                session.query(EmailModel)
                .filter_by(message_id = message_id)
                .first()
            )

            if model is None:
                return None

            return model_to_email(model)

        finally:
            session.close()

        
    def list(self) -> list[Email]:
        session = self.database.get_session()

        try:

            models = session.query(EmailModel).all()

            return [
                model_to_email(model)
                for model in models
            ]

        finally:

            session.close()