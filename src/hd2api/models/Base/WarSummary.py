from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel

from .GalaxyStats import GalaxyStats
from .PlanetStats import PlanetStats


class WarSummary(BaseApiModel):
    """
    General statistics about the galaxy and any specific planets that the community has played on.

    """

    galaxy_stats: Optional[GalaxyStats] = Field(
        alias="galaxy_stats",
        default=None,
        description="Contains galaxy wide statistics aggregated from all planets.",
    )

    planets_stats: Optional[List[Optional[PlanetStats]]] = Field(
        alias="planets_stats",
        default=None,
        description="List of statistics for specific planets if the community has fought on said planet previously.",
    )
