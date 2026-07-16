import httpx
from datetime import datetime

from app.domain.email import Email
from app.providers.base import EmailProvider
from app.providers.auth.base import AuthenticationProvider

class GraphEmailProvider(EmailProvider):

    GRAPH_URL = (
        "https://graph.microsoft.com/v1.0"
    )
    SCOPES = ["Mail.Read"]

    def __init__(
        self,
        authenticator: AuthenticationProvider
    ):

        self.authenticator = authenticator


    def fetch_unread(self) -> list[Email]:

        
        token = self.authenticator.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }


        params = {
            "$filter": "isRead eq false",
            "$top": 10,
            "$select": (
                "id,"
                "internetMessageId,"
                "subject,"
                "sender,"
                "toRecipients,"
                "receivedDateTime,"
                "body,"
                "isRead,"
                "hasAttachments"
            )
        }


        response = httpx.get(
            f"{self.GRAPH_URL}/me/messages",
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            print("GRAPH ERROR")
            print(response.status_code)
            print(response.text)

        response.raise_for_status()


        data = response.json()


        return [
            self._map_email(item)
            for item in data["value"]
        ]


    def _map_email(
        self,
        item: dict
    ) -> Email:

        sender = (
            item
            .get("sender", {})
            .get("emailAddress", {})
            .get("address")
        )

        recipients = []

        for recipient in item.get("toRecipients", []):
            recipients.append(
                recipient["emailAddress"]["address"]
            )

        return Email(
            uid = None,

            message_id=(
                item.get("internetMessageId")
                or item["id"]
            ),

            subject=item.get("subject", ""),

            sender=sender,

            recipients=recipients,

            
            date=datetime.fromisoformat(
                item["receivedDateTime"]
                .replace("Z", "+00:00")
            ),

            body=(
                item
                .get("body", {})
                .get("content", "")
            ),

            is_read=item.get(
                "isRead",
                False
            ),

            has_attachments=item.get(
                "hasAttachments",
                False
            ),

            attachments=[]
        )