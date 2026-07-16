import jwt
import httpx

from app.core.config import settings
from app.providers.graph import GraphEmailProvider
from app.providers.auth.microsoft import MicrosoftAuthenticator
from app.providers.auth.token_cache import TokenCache


auth = MicrosoftAuthenticator(
    client_id=settings.azure_client_id,
    tenant_id=settings.azure_tenant_id,
    token_cache=TokenCache(),
    scopes=[
        "Mail.Read"
    ]
)


provider = GraphEmailProvider(
    authenticator=auth
)

token = auth.get_access_token()

payload = jwt.decode(
    token,
    options={
        "verify_signature": False
    }
)

print("\nTOKEN CLAIMS")
print("================")
print("aud:", payload.get("aud"))
print("scp:", payload.get("scp"))
print("iss:", payload.get("iss"))
print("================\n")

graph = "https://graph.microsoft.com/v1.0"

# had issues with personal account without exchange. this test allows to confine the issue to mailbox only
resp = httpx.get(
    f"{graph}/me",
    headers={"Authorization": f"Bearer {token}"}
)

print("GRAPH /me:", resp.status_code)
print(resp.json() if resp.status_code == 200 else resp.text)

emails = provider.fetch_unread()


for email in emails:

    print("================")
    print(email.subject)
    print(email.sender)
    print(email.body[:200])