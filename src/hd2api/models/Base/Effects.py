from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class PlanetActiveEffects(BaseApiModel):
    """
    Raw Active Planet Effects, with the planet index and the galacticEffectId

    """

    index: Optional[int] = Field(alias="index", default=None)

    galacticEffectId: Optional[int] = Field(alias="galacticEffectId", default=None)
