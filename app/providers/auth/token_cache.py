from pathlib import Path

from msal import SerializableTokenCache


class TokenCache:

    def __init__(
        self,
        path: str = "/storage/msal_cache.bin"
    ):
        self.path = Path(path)

        self.cache = SerializableTokenCache()

        if self.path.exists():
            self.cache.deserialize(
                self.path.read_text()
            )

    def save(self):

        if not self.cache.has_state_changed:
            return

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.path.write_text(
            self.cache.serialize()
        )