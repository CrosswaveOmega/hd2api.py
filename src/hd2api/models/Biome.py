from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel


class Biome(BaseApiModel):
    """
    Static information about a biome of a planet.

    """

    name: Optional[str] = Field(
        alias="name", default=None, description="The fan nickname of the biome."
    )

    description: Optional[str] = Field(
        alias="description", default=None, description="The in-game description for the biome."
    )
