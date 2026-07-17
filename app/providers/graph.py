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
    
    def fetch_since( self) -> List[Email]:

        messages = self.client.get(
            "/me/messages",
            params={
                "$top": limit,
                "$orderby": "receivedDateTime desc"
            }
        )

        return [
            self._map_message(message)
            for message in messages
        ]


    def fetch_unread(self) -> List[Email]:

        return self._fetch_messages(
            {
                "$filter": "isRead eq false",
                "$top": 50
            }
        )


    def fetch_since(
        self,
        since: datetime
    ) -> List[Email]:

        graph_date = (
            since
            .astimezone()
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        )

        return self._fetch_messages(
            {
                "$filter": f"receivedDateTime ge {graph_date}",
                "$orderby": "receivedDateTime desc"
            }
        )

    def _fetch_messages(
        self,
        extra_params: dict
    ) -> List[Email]:

        token = self.authenticator.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
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

        params.update(extra_params)

        response = httpx.get(
            f"{self.GRAPH_URL}/me/messages",
            headers=headers,
            params=params
        )

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

        recipients = [
            recipient["emailAddress"]["address"]
            for recipient in item.get(
                "toRecipients",
                []
            )
        ]

        return Email(
            uid=None,

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

            body=item.get("body", {}).get(
                "content",
                ""
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

