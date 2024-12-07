from typing import Optional

from pydantic import Field

from ...constants import rewards
from ...util.utils import select_emoji as emj
from ..ABC.model import BaseApiModel


class Reward(BaseApiModel):
    """Raw model representing a reward that will be given for the completion of an Assignment."""

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="Use Unknown. Initially thought to be the type of reward."
        + "Initally thought to be 1 for medals, recent mos have disproved"
        + "this by returning requisition which uses the same type.",
    )

    id32: Optional[int] = Field(
        alias="id32",
        default=None,
        description="Internal identifier of the resource this Reward represents. 897894480 is medals",
    )

    amount: Optional[int] = Field(
        alias="amount",
        default=None,
        description="The amount of the given resource players will receive upon completion.",
    )

    def format(self) -> str:
        """Return the string representation of any reward."""
        type = self.type
        if self.id32 in rewards:
            type = rewards[self.id32]
        if type == 1:
            return f"{emj('medal')} × {self.amount}"
        if type == 2:
            return f"{emj('req')} × {self.amount}"
        if type == 3:
            return f"{emj('credits')} × {self.amount}"

        return f"Unknown type:{self.type} × {self.amount}"
