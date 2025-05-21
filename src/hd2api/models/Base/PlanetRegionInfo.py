from typing import Optional

from pydantic import Field

from ..ABC.model import BaseApiModel


class PlanetRegionInfo(BaseApiModel):
    """
    Model representing information about a planet region from the 'WarInfo' endpoint
    returned by ArrowHead's API.
    """

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="The numerical identifier for this planet.",
    )

    regionIndex: Optional[int] = Field(
        alias="regionIndex",
        default=None,
        description="The numerical identifier for this region within the planet.",
    )

    settingsHash: Optional[int] = Field(
        alias="settingsHash",
        default=None,
        description="Hash value pointing to the internal planet settings for this region.",
    )

    maxHealth: Optional[int] = Field(
        alias="maxHealth",
        default=None,
        description="The maximum 'health' of this region, indicating how much effort is required to liberate it.",
    )

    regionSize: Optional[int] = Field(
        alias="regionSize",
        default=None,
        description="The size of this region.",
    )
