from typing import Optional, Union

from pydantic import Field

from ..ABC.model import BaseApiModel


class GlobalResource(BaseApiModel):
    """
    Raw object which represents a global resource.
    """

    id32: Optional[int] = Field(
        alias="id32", default=None, description="The 32-bit ID."
    )
    currentValue: Optional[Union[int, float]] = Field(
        alias="currentValue",
        default=None,
        description="The current value of whatever this global resource is.",
    )
    maxValue: Optional[Union[int, float]] = Field(
        alias="maxValue",
        default=None,
        description="The max value of whatever this global resource is.",
    )
    flags: Optional[int] = Field(
        alias="flags",
        default=None,
        description="Flags that indicate something about this resource.",
    )

    def __sub__(self, other: "GlobalResource") -> "GlobalResource":
        camp = GlobalResource(
            id32=self.id32,
            currentValue=self.currentValue - other.currentValue,  # type: ignore
            maxValue=self.maxValue,
            flags=self.flags,
        )
        # camp.retrieved_at = self.retrieved_at - other.retrieved_at
        return camp
