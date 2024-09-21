from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel


class KnownPlanetEffect(BaseApiModel):
    """
    A known planet effect, with a name and description.
    """

    galacticEffectId: Optional[int] = Field(alias="galacticEffectId", default=None)

    name: Optional[str] = Field(alias="name", default=None)

    description: Optional[str] = Field(alias="description", default=None)
