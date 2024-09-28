from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel

from .PlanetCoordinates import PlanetCoordinates


class PlanetInfo(BaseApiModel):
    """
    Raw model Representing information of a planet from the 'WarInfo' endpoint returned by ArrowHead's API.
    """

    index: Optional[int] = Field(
        alias="index",
        default=None,
        description="The numerical identifier for this planet, often referred to as the PlanetIndex, used to reference by other properties throughout the API (like Waypoints).",
    )

    settingsHash: Optional[int] = Field(
        alias="settingsHash",
        default=None,
        description="Hash value pointing to the internal planet settings for this world.  This is used in game.",
    )

    position: Optional[PlanetCoordinates] = Field(
        alias="position",
        default=None,
        description="A set of X/Y coordinates specifying the position of this planet on the galaxy map.",
    )

    waypoints: Optional[List[int]] = Field(
        alias="waypoints",
        default=None,
        description="A list of links to other planets (supply lines).",
    )

    sector: Optional[int] = Field(
        alias="sector",
        default=None,
        description="The identifier of the sector this planet is located in.",
    )

    maxHealth: Optional[int] = Field(
        alias="maxHealth",
        default=None,
        description="The 'health' of this planet, indicates how much liberation it needs to switch sides.",
    )

    disabled: Optional[bool] = Field(
        alias="disabled",
        default=None,
        description="Whether this planet is currently considered active in the galactic war.",
    )

    initialOwner: Optional[int] = Field(
        alias="initialOwner",
        default=None,
        description="The identifier of the faction that initially owned this planet.",
    )
