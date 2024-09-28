from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class Task(BaseApiModel):
    """
    Raw model representing a task to be completed in an Assignment.
    It's exact values are not all known at the time.

    """

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="A numerical value pertaining to the type of task to be completed."
        + "  Only the Task types the community has seen before are known, see Task2.",
    )

    values: Optional[List[int]] = Field(
        alias="values",
        default=None,
        description="A list of numerical values pertaining to the settings of this task.  ",
    )

    valueTypes: Optional[List[int]] = Field(
        alias="valueTypes",
        default=None,
        description="A list of numerical values pertaining to what each value in values reprsents."
        + " Entire list of known value types is unknown, only the values from Assignments"
        + " already recieved by the community are known, see Task2.",
    )
