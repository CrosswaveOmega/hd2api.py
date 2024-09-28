from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel

from .Planet import Planet


class Campaign2(BaseApiModel):
    """
    An ongoing campaign on a planet.

    """

    id: Optional[int] = Field(
        alias="id", default=None, description="The unique identifier of this campaign."
    )

    planet: Optional[Planet] = Field(
        alias="planet",
        default=None,
        description="The planet on which this campaign is being fought.",
    )

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="The type of campaign, this should be mapped onto an enum.",
    )

    count: Optional[int] = Field(
        alias="count",
        default=None,
        description="Indicates how many campaigns have already been fought on this Planet.",
    )

    def __sub__(self, other: "Campaign2") -> "Campaign2":
        camp = Campaign2(
            id=self.id,
            planet=self.planet - other.planet,  # type: ignore
            type=self.type,
            count=self.count,
            time_delta=self.retrieved_at - other.retrieved_at,  # type: ignore
        )
        # camp.retrieved_at = self.retrieved_at - other.retrieved_at
        return camp

    @staticmethod
    def average(changes: List["Campaign2"]) -> "Campaign2":
        first = changes[0]
        avg = Planet.average([c.planet for c in changes])
        return Campaign2(id=first.id, planet=avg, type=first.type, count=first.count)
