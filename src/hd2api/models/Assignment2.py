from typing import *
from datetime import datetime

from pydantic import Field
from .ABC.model import BaseApiModel

from .Reward2 import Reward2
from .Task2 import Task2
from .Planet import Planet
from .Base.Reward import Reward
from .ABC.utils import changeformatif as cfi
from .ABC.utils import extract_timestamp as et
from .ABC.utils import human_format as hf
from .ABC.utils import select_emoji as emj


class Assignment2(BaseApiModel):
    """
        None model
            Represents an assignment given by Super Earth to the community.
    This is also known as &#39;Major Order&#39;s in the game.

    """

    type: Optional[int] = Field(alias="type", default=None)

    flags: Optional[int] = Field(alias="flags", default=None)

    id: Optional[int] = Field(alias="id", default=None)

    progress: Optional[List[int]] = Field(alias="progress", default_factory=list)

    title: Optional[Union[str, Dict[str, Any]]] = Field(alias="title", default=None)

    briefing: Optional[Union[str, Dict[str, Any]]] = Field(alias="briefing", default=None)

    description: Optional[Union[str, Dict[str, Any]]] = Field(alias="description", default=None)

    tasks: Optional[List[Task2]] = Field(alias="tasks", default_factory=list)

    reward: Optional[Reward2] = Field(alias="reward", default=None)

    rewards: Optional[List[Optional[Reward]]] = Field(alias="rewards", default=None)

    expiration: Optional[str] = Field(alias="expiration", default=None)

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