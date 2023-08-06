import os
from typing import Optional, cast
from .workspaces import Workspaces
from .devices import Devices
from .connected_accounts import ConnectedAccounts
from .connect_webviews import ConnectWebviews
from .locks import Locks
from .access_codes import AccessCodes
from .action_attempts import ActionAttempts
from .types import AbstractSeam


class Seam(AbstractSeam):
    api_key: str
    api_url: str = "https://connect.getseam.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
    ):
        if api_key is None:
            api_key = os.environ.get("SEAM_API_KEY", None)
        if api_key is None:
            raise Exception(
                "SEAM_API_KEY not found in environment, and api_key not provided"
            )
        if api_url is None:
            api_url = os.environ.get("SEAM_API_URL", self.api_url)
        self.api_key = api_key
        self.api_url = cast(str, api_url)
        self.workspaces = Workspaces(seam=self)
        self.connected_accounts = ConnectedAccounts(seam=self)
        self.connect_webviews = ConnectWebviews(seam=self)
        self.devices = Devices(seam=self)
        self.locks = Locks(seam=self)
        self.access_codes = AccessCodes(seam=self)
        self.action_attempts = ActionAttempts(seam=self)
