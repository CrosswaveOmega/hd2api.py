from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class JointOperation(BaseApiModel):
    """
    Raw model representing a joint operation.  Typically seen with planetary defense campaigns, but exact use is unknown.

    """

    id: Optional[int] = Field(
        alias="id", default=None, description="Unique identifier for this joint operation."
    )

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="Planet index this joint operation is happening on.",
    )

    hqNodeIndex: Optional[int] = Field(
        alias="hqNodeIndex", default=None, description="Use unknown."
    )
