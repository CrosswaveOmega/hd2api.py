from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel


class SteamNews(BaseApiModel):
    """
    Represents a new article from Steam's news feed.

    """

    id: Optional[str] = Field(
        alias="id", default=None, description="The identifier assigned by Steam to this news item."
    )

    title: Optional[str] = Field(
        alias="title", default=None, description="The title of the Steam news item."
    )

    url: Optional[str] = Field(
        alias="url", default=None, description="The URL to Steam where this news item was posted."
    )

    author: Optional[str] = Field(
        alias="author", default=None, description="The author who posted this message on Steam."
    )

    content: Optional[str] = Field(
        alias="content",
        default=None,
        description="The message posted by Steam, currently in Steam's weird markdown format.",
    )

    publishedAt: Optional[str] = Field(
        alias="publishedAt", default=None, description="When this message was posted."
    )
