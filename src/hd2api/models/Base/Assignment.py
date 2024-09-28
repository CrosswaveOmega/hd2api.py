from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel

from .Setting import Setting


class Assignment(BaseApiModel):
    """
    Raw Model representing an assignment given from Super Earth to the Helldivers.

    """

    id32: Optional[int] = Field(
        alias="id32", default=None, description="Internal identifier of this assignment."
    )

    progress: Optional[List[int]] = Field(
        alias="progress",
        default=None,
        description="A list of numbers representing progress in the assignment.",
    )

    expiresIn: Optional[int] = Field(
        alias="expiresIn",
        default=None,
        description="The amount of seconds until this assignment expires.",
    )

    setting: Optional[Setting] = Field(
        alias="setting",
        default=None,
        description="Contains detailed information on this assignment like briefing, rewards, ...",
    )
