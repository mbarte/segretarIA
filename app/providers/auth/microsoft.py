from msal import PublicClientApplication

from .base import AuthenticationProvider
from .token_cache import TokenCache

class MicrosoftAuthenticator(AuthenticationProvider):

    SCOPES = [
        "https://outlook.office.com/IMAP.AccessAsUser.All"
    ]

    def __init__(
        self,
        client_id: str,
        tenant_id: str,
        redirect_uri: str,
        token_cache: TokenCache
    ):

        self.client_id = client_id
        self.tenant_id = tenant_id
        self.redirect_uri = redirect_uri

        self.token_cache = token_cache

        self.app = PublicClientApplication(
            client_id = self.client_id,
            authority =(
                f"https://login.microsoftonline.com/{tenant_id}"
            ),
            token_cache = self.token_cache.cache
        )

    def login(self):

        flow = self.app.initiate_device_flow(
            scopes=self.SCOPES
        )

        if "user_code" not in flow:
            raise RuntimeError(
                "Impossibile creare device flow"
            )

        print(flow["message"])

        result = self.app.acquire_token_by_device_flow(flow)

        self.token_cache.save()

        return result

    def get_access_token(self)-> str:
        accounts = self.app.get_accounts()

        if accounts:

            result = self.app.acquire_token_silent(
                scopes = self.SCOPES,
                account = accounts[0]
            )

            if result and "access_token" in result:
                self.token_cache.save()

                return result["access_token"]

        result = self.login()

        if "access_token" not in result:

            raise RuntimeError(
                result.get(
                    "error_description",
                    "Authentication failed"
                )
            )

        self.token_cache.save()
        return result["access_token"]

    def debug_token(self):

        accounts = self.app.get_accounts()

        result = self.app.acquire_token_silent(
            scopes=self.SCOPES,
            account=accounts[0]
        )

        return result

    