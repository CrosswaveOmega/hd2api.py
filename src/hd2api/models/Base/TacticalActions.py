from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel

from .Cost import Cost


class TacticalAction(BaseApiModel):
    """Raw model that's a DSS Tactical action"""

    id32: Optional[int] = Field(
        alias="id32",
        default=None,
        description="Internal identifier of this tactical action",
    )

    mediaId32: Optional[int] = Field(
        alias="id32",
        default=None,
        description="Internal identifier of this tactical action's media",
    )

    name: Optional[str] = Field(
        alias="name", default=None, description="The name of this tactical action."
    )

    description: Optional[str] = Field(
        alias="description",
        default=None,
        description="The description of this tactical action.",
    )

    strategicDescription: Optional[str] = Field(
        alias="strategicDescription",
        default=None,
        description="The strategic description of this tactical action.",
    )

    status: Optional[int] = Field(
        alias="status",
        default=None,
        description="Integer representing status",
    )

    statusExpireAtWarTimeSeconds: Optional[int] = Field(
        alias="statusExpireAtWarTimeSeconds",
        default=None,
        description="War time when the tactical action will expire",
    )

    expiration: Optional[str] = Field(
        alias="expiration",
        default=None,
        description="The estimated date when the current voting period will expire.",
    )

    cost: Optional[List[Cost]] = Field(
        alias="cost", default_factory=list, description="List of costs."
    )

    effectIds: Optional[List[int]] = Field(
        alias="effectIds", default_factory=list, description="List of effect IDs."
    )

    activeEffectIds: Optional[List[int]] = Field(
        alias="activeEffectIds", default_factory=list, description="List of active effect IDs."
    )
