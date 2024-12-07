from typing import Any, Dict, Optional, Tuple, Union

from pydantic import Field

from ..util.utils import extract_timestamp as et
from ..util.utils import hdml_parse
from .ABC.model import BaseApiModel


class Dispatch(BaseApiModel):
    """
    A message from high command to the players, usually updates on the status of the war effort.

    """

    id: Optional[int] = Field(
        alias="id", default=None, description="The unique identifier of this dispatch."
    )

    published: Optional[str] = Field(
        alias="published",
        default=None,
        description="Datetime when the dispatch was published, relative to the wartime..",
    )

    type: Optional[int] = Field(
        alias="type", default=None, description="The type of dispatch, purpose unknown."
    )

    message: Optional[Union[str, Dict[str, Any]]] = Field(
        alias="message",
        default=None,
        description="The message this dispatch represents.  This is formatted in a special 'helldives markup language' used by the game.",
    )

    def get_text_and_time(self) -> Tuple[str, Optional[str]]:
        # Replace the matched patterns with markdown bold syntax
        converted_text = hdml_parse(self.message)
        extract_time = et(self.published)
        return converted_text, extract_time
