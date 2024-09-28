from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel
from ...util.utils import hdml_parse
import re


class NewsFeedItem(BaseApiModel):
    """
    Represents an item in the newsfeed of Super Earth.

    """

    id: Optional[int] = Field(
        alias="id", default=None, description="The identifier of this newsfeed item."
    )

    published: Optional[int] = Field(
        alias="published",
        default=None,
        description="The internal game wartime (See WarStatus) when this NewsFeedItem  ",
    )

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="A numerical type supposedly for the type of NewsFeed item, purpose unknown.",
    )

    tagIds: Optional[List[Union[str, int]]] = Field(
        alias="tagIds",
        default_factory=list,
        description="Use unknown, a list of tags attached to each news_feed item.",
    )

    message: Optional[str] = Field(
        alias="message",
        default=None,
        description="A message containing areadable text, formatted in a special 'helldives markup language' used by the game.",
    )

    def to_str(self) -> Tuple[str, str]:
        # message=self.# Replace the matched patterns with markdown bold syntax
        converted_text = hdml_parse(self.message if self.message else "INVALID")
        extract_time = self.published
        return (
            f"Dispatch {self.id}, type {self.type}",
            f"{converted_text}\n published at: {(extract_time)}",
        )
