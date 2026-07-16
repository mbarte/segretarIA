from app.core.config import settings
from app.providers.imap import IMAPProvider
from app.providers.auth.microsoft import MicrosoftAuthenticator
from app.providers.auth.token_cache import TokenCache


auth = MicrosoftAuthenticator(
    client_id=settings.azure_client_id,
    tenant_id=settings.azure_tenant_id,
    scopes=["https://outlook.office.com/IMAP.AccessAsUser.All"],
    token_cache=TokenCache()
)


provider = IMAPProvider(
    server="outlook.office365.com",
    port=993,
    username=settings.email_address,
    authenticator=auth
)


result = auth.debug_token()

print(result.keys())
print(result.get("scope"))
print(result.get("access_token")[:50])


emails = provider.fetch_unread()
for email in emails:

    print("================")
    print(email.subject)
    print(email.sender)
    print(email.body[:200])