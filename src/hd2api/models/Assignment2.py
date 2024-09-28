from typing import *
from datetime import datetime

from pydantic import Field
from .ABC.model import BaseApiModel

from .Reward2 import Reward2
from .Task2 import Task2
from .Planet import Planet
from .Base.Reward import Reward
from ..util.utils import changeformatif as cfi
from ..util.utils import extract_timestamp as et
from ..util.utils import human_format as hf


class Assignment2(BaseApiModel):
    """
    An assignment given by Super Earth to the community. This is also known as Major Orders game.

    """

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="The type of assignment, values unknown at the moment.",
    )

    flags: Optional[int] = Field(
        alias="flags",
        default=None,
        description="Flags, suspected to be a binary OR'd value, purpose unknown.",
    )

    id: Optional[int] = Field(
        alias="id", default=None, description="The unique identifier of this assignment."
    )

    progress: Optional[List[int]] = Field(
        alias="progress",
        default_factory=list,
        description="A list of numbers representing progress in the assignment, pertaining to each task.",
    )

    title: Optional[Union[str, Dict[str, Any]]] = Field(
        alias="title",
        default=None,
        description="The title of the assignment.  Usually just 'MAJOR ORDER' in all caps.",
    )

    briefing: Optional[Union[str, Dict[str, Any]]] = Field(
        alias="briefing",
        default=None,
        description="A long form description of the assignment, usually contains context.",
    )

    description: Optional[Union[str, Dict[str, Any]]] = Field(
        alias="description", default=None, description="A very short summary of the description."
    )

    tasks: Optional[List[Task2]] = Field(
        alias="tasks",
        default_factory=list,
        description="A list of tasks that need to be completed for this assignment.",
    )

    reward: Optional[Reward2] = Field(
        alias="reward",
        default=None,
        description="The primary reward for completing the assignment.",
    )

    rewards: Optional[List[Optional[Reward2]]] = Field(
        alias="rewards",
        default=None,
        description="A list of rewards for completing the assignment.",
    )

    expiration: Optional[str] = Field(
        alias="expiration",
        default=None,
        description="The estimated date when the assignment will expire.",
    )

    def __sub__(self, other: "Assignment2") -> "Assignment2":
        new_progress = [s - o for s, o in zip(self.progress, other.progress)]

        retrieved_at = self.retrieved_at
        other_retrieved_at = other.retrieved_at

        time_delta = retrieved_at - other_retrieved_at  # type: ignore

        new_progress = [s - o for s, o in zip(self.progress, other.progress)]
        return Assignment2(
            id=self.id,
            progress=new_progress,
            title=self.title,
            flags=self.flags,
            briefing=self.briefing,
            description=self.description,
            tasks=self.tasks,
            reward=self.reward,
            rewards=self.rewards,
            expiration=self.expiration,
            time_delta=time_delta,
            retrieved_at=retrieved_at,
        )

    def get_task_planets(self) -> List[int]:
        planets = []
        for e, task in enumerate(self.tasks):
            task_type, taskdata = task.taskAdvanced()

            if taskdata.planet:
                for p in taskdata.planet:
                    planets.append(p)
        return planets

    def to_str(self) -> str:
        planets = {}
        progress = self.progress
        tasks = ""
        exptime = et(self.expiration).isoformat()
        for e, task in enumerate(self.tasks):
            task_type, taskdata = task.taskAdvanced()
            tasks += task.task_str(progress[e], e, planets) + "\n"
        tex = f"{self.briefing},by {exptime}\n{tasks}"

        return tex
