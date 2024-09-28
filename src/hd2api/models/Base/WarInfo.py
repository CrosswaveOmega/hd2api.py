from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel

from .HomeWorld import HomeWorld
from .PlanetInfo import PlanetInfo


class WarInfo(BaseApiModel):
    """
    Mostly static information on the current galactic war.
    This includes information on each planet, homeworlds, supply lines, the current warID,
    and more.

    """

    warId: Optional[int] = Field(
        alias="warId",
        default=None,
        description="The identifier of the war season this WarInfo represents.",
    )

    startDate: Optional[int] = Field(
        alias="startDate",
        default=None,
        description="A unix timestamp (in seconds) when this season started.",
    )

    endDate: Optional[int] = Field(
        alias="endDate",
        default=None,
        description="A unix timestamp (in seconds) when this season will end.",
    )

    layoutVersion: Optional[int] = Field(
        alias="layoutVersion",
        default=None,
        description="Use unknown. Value tends to increase whenever the waypoints change.",
    )

    minimumClientVersion: Optional[str] = Field(
        alias="minimumClientVersion",
        default=None,
        description="A version string indicating the minimum game client version the API supports.",
    )

    planetInfos: Optional[List[Optional[PlanetInfo]]] = Field(
        alias="planetInfos",
        default_factory=list,
        description="A list of planets involved in this season's war.",
    )

    homeWorlds: Optional[List[Optional[HomeWorld]]] = Field(
        alias="homeWorlds",
        default_factory=list,
        description="A list of homeworlds for the races (factions) involved in this war.",
    )

    capitalInfos: Optional[List[Any]] = Field(
        alias="capitalInfos",
        default_factory=list,
        description="Capital information related to the war.  Unused.",
    )

    planetPermanentEffects: Optional[List[Any]] = Field(
        alias="planetPermanentEffects",
        default_factory=list,
        description="List of permanent effects on planets.  Unused.",
    )
