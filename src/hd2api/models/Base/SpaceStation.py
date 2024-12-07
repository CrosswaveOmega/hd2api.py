from typing import List, Optional

from pydantic import Field

from ..ABC.model import BaseApiModel
from .TacticalActions import TacticalAction


class SpaceStationStatus(BaseApiModel):
    """Raw model representing a single space station in the WarStatus object"""

    id32: Optional[int] = Field(
        alias="id32",
        default=None,
        description="Internal identifier of which Space Station this is.",
    )

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="Planet Index this station is over",
    )

    activeEffectIds: Optional[List[int]] = Field(
        alias="activeEffectIds", default_factory=list, description="List of effect IDs."
    )

    flags: Optional[int] = Field(
        alias="flags", default=None, description="The flag associated with the station."
    )

    currentElectionEndWarTime: Optional[int] = Field(
        alias="currentElectionEndWarTime",
        default=None,
        description="Election end war time.  significance unknown",
    )


class SpaceStation(BaseApiModel):
    """Raw model representing a single space station's full details."""

    id32: Optional[int] = Field(
        alias="id32",
        default=None,
        description="Internal identifier of which Space Station this is.",
    )
    lastElectionId: Optional[str] = Field(
        alias="lastElectionId",
        default=None,
        description="ID for the last election period to move the Space Station.",
    )

    currentElectionId: Optional[str] = Field(
        alias="currentElectionId",
        default=None,
        description="ID for the current election period to move the Space Station.",
    )

    nextElectionId: Optional[str] = Field(
        alias="nextElectionId",
        default=None,
        description="ID for the next election period to move the Space Station.",
    )

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="Planet Index this station is over",
    )

    flags: Optional[int] = Field(
        alias="flags", default=None, description="The flag associated with the station."
    )

    currentElectionEndWarTime: Optional[int] = Field(
        alias="currentElectionEndWarTime",
        default=None,
        description="War Time when the current election period ends and the Station will move to the next planet.",
    )

    tacticalActions: Optional[List[TacticalAction]] = Field(
        alias="tacticalActions",
        default_factory=list,
        description="List of all tactical actions in progress by this station.",
    )
