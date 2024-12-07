from typing import Optional

from pydantic import Field

from ..ABC.model import BaseApiModel


class Cost(BaseApiModel):
    """Raw model that's the cost for maintaining a DSS Tactical action"""

    id: Optional[str] = Field(
        alias="id",
        default=None,
        description="Internal identifier of this cost.",
    )

    itemMixId: Optional[int] = Field(
        alias="itemMixId",
        default=None,
        description="MIX ID for item resource.",
    )

    targetValue: Optional[int] = Field(
        alias="targetValue",
        default=None,
        description="Target amount of resource.",
    )

    currentValue: Optional[float] = Field(
        alias="currentValue",
        default=None,
        description="current value for resource",
    )

    deltaPerSecond: Optional[float] = Field(
        alias="deltaPerSecond",
        default=None,
        description="current value for resource",
    )

    maxDonationAmount: Optional[int] = Field(
        alias="maxDonationAmount",
        default=None,
        description="Max amount of resources that can be donated by one helldiver",
    )

    maxDonationPeriodSeconds: Optional[int] = Field(
        alias="maxDonationPeriodSeconds",
        default=None,
        description="time  that can be donated by one helldiver",
    )
