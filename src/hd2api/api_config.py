import os
from typing import Literal, Optional, Union

# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
from .models import StaticAll, GalaxyStatic, EffectStatic
from .load_json import load_and_merge_json_files


class APIConfig(BaseModel):
    """Configuration object for the api wrappers.

    Attributes:
        api_comm (str): Base path for the community API.

        api_diveharder (str): Base path for the Diveharder API.

        api_direct (str): Base path for the game's direct API.

        use_raw (Literal["community", "diveharder", "direct"]): The source to use, default is "diveharder".

        verify (Union[bool, str]): Unused.

        client_name (str): Name sent to the client, default is "DefaultClientName".

        language (str): The accept-language sent to the client, default is "en-US".

        static_path (str): Path for static files.

        access_token (Optional[str]): Unused.

        statics (Optional[StaticAll]): Static files.
    """

    api_comm: str = "https://api.helldivers2.dev"  # Base path for the community API

    api_diveharder: str = "https://api.diveharder.com"  # Base path for the Diveharder API

    api_direct: str = "https://api.live.prod.thehelldiversgame.com"  # Base path for the game's API directly

    use_raw: Literal["community", "diveharder", "direct"] = "diveharder"
    verify: Union[bool, str] = True  # Unused
    client_name: str = "DefaultClientName"  # Name sent to the client
    language: str = "en-US"  # The accept-language sent to the client
    static_path: str = ""  # Path for static files
    access_token: Optional[str] = None  # Unused
    statics: Optional[StaticAll] = None  # Static files

    def staticdata(self):
        planetjson = load_and_merge_json_files("planets", self.static_path)
        effectjson = load_and_merge_json_files("effects", self.static_path)
        self.statics = StaticAll(
            galaxystatic=GalaxyStatic(**planetjson),
            effectstatic=EffectStatic(**effectjson),
        )
        return self.statics

    def get_access_token(self) -> Optional[str]:
        """There really isn't an access token."""
        try:
            return self.access_token
        except KeyError:
            return None

    def get_client_name(self):
        try:
            return self.client_name
        except KeyError:
            return None

    def set_access_token(self, value: str):
        self.access_token = value


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code} {message}")

    def __str__(self):
        return f"{self.status_code} {self.message}"
