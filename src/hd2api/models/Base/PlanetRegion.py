from typing import Optional

from pydantic import Field, model_validator, root_validator

from ..ABC.model import BaseApiModel


class PlanetRegion(BaseApiModel):
    """
    Raw model representing the 'current' state of a planet in the galactic war.
    """

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="The planet index of the planet this status object refers to, based on WarInfo.",
    )

    regionIndex: Optional[int] = Field(
        alias="regionIndex",
        default=None,
        description="The region index within the planet this status object refers to.",
    )

    owner: Optional[int] = Field(
        alias="owner",
        default=None,
        description="The faction currently owning the region.",
    )

    health: Optional[int] = Field(
        alias="health",
        default=None,
        description="The current health / liberation of the region.",
    )

    regenPerSecond: Optional[float] = Field(
        alias="regenPerSecond",
        default=None,
        description="If left alone, how much the health of the region would regenerate.",
    )

    availabilityFactor: Optional[float] = Field(
        alias="availabilityFactor",
        default=None,
        description="A factor indicating the availability of the region.",
    )

    isAvailable: Optional[bool] = Field(
        alias="isAvailable",
        default=None,
        description="Whether the region is currently available.",
    )

    players: Optional[int] = Field(
        alias="players",
        default=None,
        description="The number of helldivers currently active in this region.",
    )

    @model_validator(mode="before")
    @classmethod
    def _fix_reger_typo(cls, data: dict) -> dict:
        # If the API mistakenly returns "regerPerSecond", map it to "regenPerSecond"
        if "regerPerSecond" in data and "regenPerSecond" not in data:
            data["regenPerSecond"] = data.pop("regerPerSecond")
        return data

    def __str__(self):
        return f"{self.planetIndex}-{self.regionIndex}-{self.owner}-{self.regenPerSecond}-{self.health}"

    def __repr__(self):
        return f"{self.planetIndex}-{self.regionIndex}-{self.owner}-{self.regenPerSecond}-{self.health}"
