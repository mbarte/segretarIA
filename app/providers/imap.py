import imaplib
import email
from datetime import datetime
from email.header import decode_header
from datetime import datetime
from typing import List

from app.domain.email import Email
from app.providers.base import EmailProvider
from app.providers.auth.base import AuthenticationProvider


class IMAPProvider(EmailProvider):

    SCOPES = ["https://outlook.office.com/IMAP.AccessAsUser.All"]

    def __init__(
        self,
        server: str,
        port: int,
        username: str,
        authenticator: AuthenticationProvider
    ):
        self.server = server
        self.port = port
        self.username = username
        self.authenticator = authenticator

    def test_connection(self):

        mail = imaplib.IMAP4_SSL(
            self.server,
            self.port
        )

        access_token = self.authenticator.get_access_token()

        def auth_callback(response):
            return (
                f"user={self.username}\1"
                f"auth=Bearer {access_token}\1\1"
            ).encode()


        result = mail.authenticate(
            "XOAUTH2",
            auth_callback
        )


        print("AUTH RESULT:")
        print(result)


        mail.logout()

        print("IMAP OAuth2 OK")


    def fetch_unread(self) -> List[Email]:
        return self._fetch("UNSEEN")

    
    def fetch_since(
        self,
        since: datetime
    ) -> List[Email]:

        criteria = since.strftime("%d-%b-%Y")

        return self._fetch(
            f'(SINCE "{criteria}")'
        )

    def _fetch(self, search_criteria: str) -> List[Email]:

        emails = []

        mail = imaplib.IMAP4_SSL(
            self.server,
            self.port
        )

        access_token = self.authenticator.get_access_token()
        
        def auth_callback(response):
            return (
                f"user={self.username}\1"
                f"auth=Bearer {access_token}\1\1"
            ).encode()


        mail.authenticate(
            "XOAUTH2",
            auth_callback
        )

        mail.select("INBOX")

        status, messages = mail.uid(
            "search",
            None,
            search_criteria
        )

        if status != "OK":
            return []


        for uid in messages[0].split():

            status, data = mail.fetch(
                uid,
                "(RFC822)"
            )

            if status != "OK":
                continue


            raw_email = data[0][1]

            msg = email.message_from_bytes(
                raw_email
            )


            parsed = self._parse_email(
                uid.decode(),
                msg
            )

            emails.append(parsed)


        mail.logout()

        return emails



    def _parse_email(
        self,
        uid: str,
        msg
    ) -> Email:


        subject = self._decode_header(
            msg.get("Subject")
        )

        sender = self._decode_header(
            msg.get("From")
        )


        body = self._extract_body(
            msg
        )


        return Email(
            uid=uid,
            message_id=msg.get("Message-ID"),
            sender=sender,
            subject=subject,
            body=body,
            date=self._parse_date(
                msg.get("Date")
            ),
            is_read=False,
            recipients=[],
            has_attachments=False,
            attachments=[]
        )



    def _decode_header(self, value):

        if not value:
            return ""

        decoded = decode_header(value)

        result = ""

        for part, encoding in decoded:

            if isinstance(part, bytes):
                result += part.decode(
                    encoding or "utf-8",
                    errors="ignore"
                )
            else:
                result += part

        return result



    def _extract_body(self, msg):

        if msg.is_multipart():

            for part in msg.walk():

                content_type = part.get_content_type()

                if content_type == "text/plain":

                    return part.get_payload(
                        decode=True
                    ).decode(
                        errors="ignore"
                    )

        else:

            return msg.get_payload(
                decode=True
            ).decode(
                errors="ignore"
            )

        return ""
