from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class Campaign(BaseApiModel):
    """
    Raw model reguarding an ongoing campaign on a specific planetindex.

    """

    id: Optional[int] = Field(
        alias="id", default=None, description="The identifier of this campaign."
    )

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="The Index of the planet this campaign refers to.",
    )

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="A numerical type, indicates the type of campaign.",
    )

    count: Optional[int] = Field(
        alias="count",
        default=None,
        description="A numerical count, the amount of campaigns the planet has seen.",
    )
