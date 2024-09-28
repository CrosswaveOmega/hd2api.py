import os
from typing import Literal, Optional, Union

# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
from .models import StaticAll, GalaxyStatic, EffectStatic
from .load_json import load_and_merge_json_files


class APIConfig(BaseModel):
    """
    Configuration object for the API wrappers.
    """

    api_comm: str = Field(
        default="https://api.helldivers2.dev", description="Base path for the community API"
    )
    api_diveharder: str = Field(
        default="https://api.diveharder.com", description="Base path for the Diveharder API"
    )
    api_direct: str = Field(
        default="https://api.live.prod.thehelldiversgame.com",
        description="Base path for the game's API directly",
    )
    use_raw: Literal["community", "diveharder", "direct"] = Field(
        default="diveharder", description="The source to use, default is 'diveharder'"
    )
    verify: Union[bool, str] = Field(default=True, description="Unused")
    client_name: str = Field(default="DefaultClientName", description="Name sent to the client")
    language: str = Field(default="en-US", description="The accept-language sent to the client")
    static_path: str = Field(
        default="",
        description="Override Path for the static json files used by this library's builders",
    )
    access_token: Optional[str] = Field(default=None, description="Unused")
    statics: Optional[StaticAll] = Field(default=None, description="Cached static files")

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
