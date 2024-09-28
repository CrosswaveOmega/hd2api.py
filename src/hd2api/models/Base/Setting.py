from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel

from .Reward import Reward
from .Task import Task


class Setting(BaseApiModel):
    """
    Raw model containing the details of an Assignment, such as the reward upon completion and requirements to compete the assignmient.

    """

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="The type of assignment, values unknown at the moment.",
    )

    overrideTitle: Optional[str] = Field(
        alias="overrideTitle", default=None, description="The title of this assignment."
    )

    overrideBrief: Optional[str] = Field(
        alias="overrideBrief",
        default=None,
        description="The briefing (description) of this assignment.",
    )

    taskDescription: Optional[str] = Field(
        alias="taskDescription",
        default=None,
        description="A description of what is expected of Helldivers to complete the assignment.",
    )

    tasks: Optional[List[Optional[Task]]] = Field(
        alias="tasks",
        default=None,
        description="A list of Tasks describing the assignment requirements.",
    )

    reward: Optional[Reward] = Field(
        alias="reward",
        default=None,
        description="Contains information on the first reward players will receive upon completion.",
    )

    rewards: Optional[List[Optional[Reward]]] = Field(
        alias="rewards",
        default=None,
        description="A list of rewards for the assignment upon completion.",
    )

    flags: Optional[int] = Field(
        alias="flags",
        default=None,
        description="Flags, suspected to be a binary OR'd value, purpose unknown.",
    )
