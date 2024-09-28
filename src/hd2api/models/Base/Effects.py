from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class PlanetActiveEffects(BaseApiModel):
    """
    Raw Active Planet Effects, with the planet index and the galacticEffectId.
    Planet effects are applied to specific worlds.

    """

    index: Optional[int] = Field(
        alias="index", default=None, description="The planet index this effect is applied to"
    )

    galacticEffectId: Optional[int] = Field(
        alias="galacticEffectId",
        default=None,
        description="The effect id of the effect in question.",
    )
