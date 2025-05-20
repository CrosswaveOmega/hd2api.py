from typing import List, Optional

from pydantic import Field

from ..ABC.model import BaseApiModel
from .PlanetCoordinates import PlanetCoordinates


class PlanetRegionInfo(BaseApiModel):
    """
    Raw model Representing information of a planet from the 'WarInfo' endpoint returned by ArrowHead's API.
    """

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="The numerical identifier for this planet, often referred to as the PlanetIndex, used to reference by other properties throughout the API (like Waypoints).",
    )

    regionIndex: Optional[int] = Field(
        alias="regionIndex",
        default=None,
        description="The numerical identifier for this planet, often referred to as the PlanetIndex, used to reference by other properties throughout the API (like Waypoints).",
    )

    settingsHash: Optional[int] = Field(
        alias="settingsHash",
        default=None,
        description="Hash value pointing to the internal planet settings for this world.  This is used in game.",
    )

    maxHealth: Optional[int] = Field(
        alias="maxHealth",
        default=None,
        description="The 'health' of this planet, indicates how much liberation it needs to switch sides.",
    )

    regionSize: Optional[int] = Field(
        alias="regionSize",
        default=None,
        description="The 'health' of this planet, indicates how much liberation it needs to switch sides.",
    )
