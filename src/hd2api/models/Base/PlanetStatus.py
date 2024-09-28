from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class PlanetStatus(BaseApiModel):
    """
    Raw model Representing the 'current' state of a planet in the galactic war.

    """

    index: Optional[int] = Field(
        alias="index",
        default=None,
        description="The planet Index of the planet this status object refers to, based on WarInfo",
    )

    owner: Optional[int] = Field(
        alias="owner", default=None, description="The faction currently owning the planet."
    )

    health: Optional[int] = Field(
        alias="health", default=None, description="The current health / liberation of a planet."
    )

    regenPerSecond: Optional[float] = Field(
        alias="regenPerSecond",
        default=None,
        description="If left alone, how much the health of the planet would regenerate.",
    )

    players: Optional[int] = Field(
        alias="players",
        default=None,
        description="The amount of helldivers currently active on this planet.",
    )

    def __str__(self):
        return f"{self.index}-{self.owner}-{self.regenPerSecond}"

    def __repr__(self):
        return f"{self.index}-{self.owner}-{self.regenPerSecond}"
