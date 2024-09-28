from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel


from ..util.utils import (
    human_format as hf,
    select_emoji as emj,
    changeformatif as cfi,
    extract_timestamp as et,
)

from ..constants import rewards


class Reward2(BaseApiModel):
    """
    The reward for completing an Assignment.

    """

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
        description="Internal identifier of the resource this reward represents. 897894480 is medals.",
    )

    amount: Optional[int] = Field(
        alias="amount",
        default=None,
        description="The amount of the given resource players will receive upon completion.",
    )

    def format(self):
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
