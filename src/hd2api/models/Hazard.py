from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel


class Hazard(BaseApiModel):
    """

    Static information about an environmental hazard that can be present on a Planet.

    """

    name: Optional[str] = Field(
        alias="name", default=None, description="Official or fan name for environmental hazard"
    )

    description: Optional[str] = Field(
        alias="description",
        default=None,
        description="Official description of the environmental hazard's effects",
    )
