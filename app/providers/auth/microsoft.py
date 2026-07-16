import time

import jwt
from msal import PublicClientApplication

from .base import AuthenticationProvider
from .token_cache import TokenCache

class MicrosoftAuthenticator(AuthenticationProvider):


    def __init__(
        self,
        client_id: str,
        tenant_id: str,
        scopes: list[str],
        token_cache: TokenCache
    ):

        self.client_id = client_id
        self.tenant_id = tenant_id
        self.scopes = scopes

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
            scopes=self.scopes
        )

        if "user_code" not in flow:
            raise RuntimeError(
                "Impossibile creare device flow"
            )

        print(flow["message"])

        result = self.app.acquire_token_by_device_flow(flow)

        if "access_token" not in result:
            raise RuntimeError(result)


        self.token_cache.save()

        return result

    def get_access_token(self)-> str:
        accounts = self.app.get_accounts()

        if accounts:

            result = self.app.acquire_token_silent(
                scopes = self.scopes,
                account = accounts[0]
            )

            if result and "access_token" in result:
                try:
                    payload = jwt.decode(
                        result["access_token"],
                        options={"verify_signature": False}
                    )
                    if payload.get("exp", 0) > time.time():
                        self.token_cache.save()
                        return result["access_token"]
                except Exception:
                    pass

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
            scopes=self.scopes,
            account=accounts[0]
        )

        return result

    