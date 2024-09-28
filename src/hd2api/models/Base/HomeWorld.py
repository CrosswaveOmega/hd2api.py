from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class HomeWorld(BaseApiModel):
    """
    None model
        Represents information about the homeworld(s) of a given race.

    """

    race: Optional[int] = Field(
        alias="race",
        default=None,
        description="The identifier of the race (faction) this describes the homeworld of.",
    )

    planetIndices: Optional[List[int]] = Field(
        alias="planetIndices",
        default=None,
        description="A list of planet ids for the homeworlds for the given race.",
    )
