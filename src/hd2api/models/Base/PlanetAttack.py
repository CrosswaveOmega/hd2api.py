from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class PlanetAttack(BaseApiModel):
    """
    Raw model representing an attack from one in game planet to another.
    Planet Attacks are required for Liberation Campaigns
    (when a Super Earth world attacks an enemy world) and Defense Campaigns
    (when an enemy world attacks a Super Earth world).

    """

    source: Optional[int] = Field(
        alias="source",
        default=None,
        description="planetIndex of the planet where the attack originates from.",
    )

    target: Optional[int] = Field(
        alias="target", default=None, description="planetIndex of the planet that is under attack."
    )
