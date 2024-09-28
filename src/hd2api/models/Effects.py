from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel


class KnownPlanetEffect(BaseApiModel):
    """
    A known planet effect, with a name and description.
    """

    galacticEffectId: Optional[int] = Field(
        alias="galacticEffectId",
        default=None,
        description="The galacticEffectID pertaining to this Effect.",
    )

    name: Optional[str] = Field(
        alias="name", default=None, description="A fan nickname for this galactic effect."
    )

    description: Optional[str] = Field(
        alias="description",
        default=None,
        description="Either the official in game description for this galactic effect,"
        + "or a fan created description if an official description is not available.",
    )
