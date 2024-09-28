from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class Campaign(BaseApiModel):
    """
    None model
        Contains information of ongoing campaigns.

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
        description="A numerical type, indicates the type of campaign (see helldivers-2/json).",
    )

    count: Optional[int] = Field(
        alias="count",
        default=None,
        description="A numerical count, the amount of campaigns the planet has seen.",
    )
