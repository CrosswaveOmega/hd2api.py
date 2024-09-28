from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel


class Position(BaseApiModel):
    """
    A position on the galactic war map, relative to Super Earth.

    """

    x: Optional[float] = Field(alias="x", default=None, description="The X coordinate.")
    y: Optional[float] = Field(alias="y", default=None, description="The Y coordinate.")
