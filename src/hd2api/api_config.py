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
        description="Override path for the static json files used by this library's builders",
    )
    # __access_token: Optional[str] = None# Field(default=None, description="Unused")
    timeout: float = Field(default=8, description="Request timeout value for the endpoints.")
    statics: Optional[StaticAll] = Field(default=None, description="Cached static files")

    def staticdata(self) -> StaticAll:
        """If not already present, build up the model of static data."""
        planetjson = load_and_merge_json_files("planets", self.static_path)
        effectjson = load_and_merge_json_files("effects", self.static_path)
        self.statics = StaticAll(
            galaxystatic=GalaxyStatic(**planetjson),
            effectstatic=EffectStatic(**effectjson),
        )
        return self.statics

    def __get_access_token(self) -> Optional[str]:
        """There really isn't an access token, this is just in case."""
        try:
            return self.__access_token
        except KeyError:
            return None

    def get_client_name(self) -> str:
        """Get the client name."""
        try:
            return self.client_name
        except KeyError:
            return None

    def __set_access_token(self, value: str):
        self.__access_token = value


class HTTPException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code} {message}")

    def __str__(self):
        return f"{self.status_code} {self.message}"
