import os
from typing import Literal, Optional, Union

# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
from .models import StaticAll


class APIConfig(BaseModel):
    """Configuration object for the api wrappers.

    Args:
        BaseModel (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    api_comm: str = "https://api.helldivers2.dev"

    api_diveharder: str = "https://api.diveharder.com"

    api_direct: str = "https://api.live.prod.thehelldiversgame.com"

    use_raw: Literal["community", "diveharder", "direct"] = "diveharder"
    verify: Union[bool, str] = True
    client_name: str = "DefaultClientName"
    language: str = "en-US"
    static_path: str = ""
    access_token: Optional[str] = None
    statics: Optional[StaticAll] = None

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
