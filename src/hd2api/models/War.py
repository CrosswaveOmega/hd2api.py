from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel

from .Statistics import Statistics


class War(BaseApiModel):
    """
    Global information of the ongoing war.

    """

    started: Optional[str] = Field(
        alias="started", default=None, description="When this war was started."
    )

    ended: Optional[str] = Field(
        alias="ended", default=None, description="When this war will end (or has ended)."
    )

    now: Optional[str] = Field(
        alias="now",
        default=None,
        description="The time the snapshot of the war was taken, also doubles as the timestamp of which all other data dates from.",
    )

    clientVersion: Optional[str] = Field(
        alias="clientVersion",
        default=None,
        description="The minimum game client version required to play in this war.",
    )

    factions: Optional[List[str]] = Field(
        alias="factions",
        default=None,
        description="A list of factions currently involved in the war.",
    )

    impactMultiplier: Optional[float] = Field(
        alias="impactMultiplier",
        default=None,
        description="This is the factor by which influence at the end of a mission is multiplied"
        + " to calculate the impact on liberation. "
        + "This value is observed to inversely scale "
        + "with the total number of players online, "
        + "but the exact formula for calculation is unknown.",
    )

    warId: Optional[int] = Field(
        alias="warId", default=None, description="The current War Season's Identifier."
    )

    statistics: Optional[Statistics] = Field(
        alias="statistics",
        default=None,
        description="The statistics available for the galaxy wide war effort.",
    )

    def __sub__(self, other):
        war = War(
            started=self.started,
            ended=self.ended,
            now=self.now,
            clientVersion=self.clientVersion,
            factions=self.factions,
            impactMultiplier=self.impactMultiplier - other.impactMultiplier,
            statistics=self.statistics - other.statistics,
        )
        return war
