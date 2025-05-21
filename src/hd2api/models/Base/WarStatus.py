from typing import Any, List, Optional

from pydantic import Field

from ..ABC.model import BaseApiModel
from .Campaign import Campaign
from .Effects import PlanetActiveEffects
from .GlobalEvent import GlobalEvent
from .GlobalResource import GlobalResource
from .JointOperation import JointOperation
from .PlanetAttack import PlanetAttack
from .PlanetEvent import PlanetEvent
from .PlanetStatus import PlanetStatus
from .SpaceStation import SpaceStationStatus
from .PlanetRegion import PlanetRegion


class WarStatus(BaseApiModel):
    """
    Raw model representing a snapshot of the current state of the galactic war,
      including all active campaigns and the owner of each planet.

    """

    warId: Optional[int] = Field(
        alias="warId",
        default=None,
        description="The identifier for the warSeason this snapshot refers to.",
    )

    time: Optional[int] = Field(
        alias="time",
        default=None,
        description="The internal 'wartime' this snapshot was taken. Wartime is not a unix timestamp, but the total number of internal ticks that have occoured on ArrowHead's server. Prone to a phenomenon called wartime drift.",
    )

    impactMultiplier: Optional[float] = Field(
        alias="impactMultiplier",
        default=None,
        description="This is the factor by which influence at the end of a mission is multiplied to calculate the impact on liberation. This value is observed to inversely scale with the total number of players online, but the exact means of calculation is unknown.",
    )

    storyBeatId32: Optional[int] = Field(
        alias="storyBeatId32",
        default=None,
        description="Internal identifier possibly pertaining to an automated, storybeat for the galactic war, but is often set to 0.",
    )

    planetStatus: Optional[List[PlanetStatus]] = Field(
        alias="planetStatus",
        default_factory=list,
        description="List of all state for each planet in the galactic war at the current time.",
    )

    planetRegions: Optional[List[PlanetRegion]] = Field(
        alias="planetRegions",
        default_factory=list,
        description="List of all state for each planet regions in the galactic war at the current time.",
    )

    planetAttacks: Optional[List[Optional[PlanetAttack]]] = Field(
        alias="planetAttacks",
        default_factory=list,
        description="A list of attacks between currently ongoing at the time of this snapshot. Planet Attacks are required for Liberation Campaigns (when a Super Earth world attacks an enemy world) and Defense Campaigns (when an enemy world attacks a Super Earth world).",
    )

    campaigns: Optional[List[Optional[Campaign]]] = Field(
        alias="campaigns",
        default_factory=list,
        description="A list of ongoing campaigns in the galactic war.",
    )

    jointOperations: Optional[List[Optional[JointOperation]]] = Field(
        alias="jointOperations", default=[], description="A list of JointOperations."
    )

    planetEvents: Optional[List[Optional[PlanetEvent]]] = Field(
        alias="planetEvents", default=[], description="A list of ongoing PlanetEvents."
    )

    communityTargets: Optional[List[Any]] = Field(
        alias="communityTargets",
        default=[],
        description="A list of 'community targets', which have not been used yet by ArrowHead.",
    )
    activeElectionPolicyEffects: Optional[List[Any]] = Field(
        alias="activeElectionPolicyEffects",
        default=[],
        description="Use currently unknown.",
    )
    planetActiveEffects: Optional[List[PlanetActiveEffects]] = Field(
        alias="planetActiveEffects",
        default=[],
        description="A list of active planet effects.",
    )

    globalEvents: Optional[List[GlobalEvent]] = Field(
        alias="globalEvents",
        default=[],
        description="All current global events, including major orders",
    )
    spaceStations: Optional[List[SpaceStationStatus]] = Field(
        alias="spaceStations",
        default_factory=list,
        description="A list of 'spaceStations', which has not been used yet by ArrowHead.",
    )
    globalResources: Optional[List[GlobalResource]] = Field(
        alias="globalResources",
        default=[],
        description="A list of 'global resources', which first appear to be tied to 'gravitational waves'.",
    )

    superEarthWarResults: Optional[List[Any]] = Field(
        alias="superEarthWarResults",
        default=[],
        description="Possibly results of Super Earth's engagements during prior galactic wars. Use otherwise unknown.",
    )

    layoutVersion: Optional[int] = Field(
        alias="layoutVersion",
        default=None,
        description="Use unknown. Value tends to increase whenever the waypoints change.",
    )
