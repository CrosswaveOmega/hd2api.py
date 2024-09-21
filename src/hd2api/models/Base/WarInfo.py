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

    warId: Optional[int] = Field(alias="warId", default=None)

    startDate: Optional[int] = Field(alias="startDate", default=None)

    endDate: Optional[int] = Field(alias="endDate", default=None)

    minimumClientVersion: Optional[str] = Field(alias="minimumClientVersion", default=None)

    planetInfos: Optional[List[Optional[PlanetInfo]]] = Field(alias="planetInfos", default_factory=list)

    homeWorlds: Optional[List[Optional[HomeWorld]]] = Field(alias="homeWorlds", default_factory=list)

    capitalInfos: Optional[List[Any]] = Field(alias="capitalInfos", default_factory=list)

    planetPermanentEffects: Optional[List[Any]] = Field(alias="planetPermanentEffects", default_factory=list)
