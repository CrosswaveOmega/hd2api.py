from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class WarId(BaseApiModel):
    """
    Raw model Representing the ID of the current war returned from the WarID endpoint.

    """

    id: Optional[int] = Field(
        alias="id",
        default=None,
        description="The internal identifier for the current galactic war iteration.",
    )
