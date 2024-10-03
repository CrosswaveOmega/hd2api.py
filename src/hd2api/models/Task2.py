from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel
import json
from .Planet import Planet

from ..util.utils import changeformatif as cfi
from ..util.utils import extract_timestamp as et
from ..util.utils import human_format as hf

from ..constants import task_types, value_types, faction_names, samples, enemies


class TaskData(BaseApiModel):
    """Model that collates each value array and value_types array together."""

    faction: Optional[List[int]] = Field(alias="faction", default=None)
    hasCount: Optional[List[int]] = Field(alias="hasCount", default=None)
    goal: Optional[List[int]] = Field(alias="goal", default=None)
    enemyID: Optional[List[int]] = Field(alias="enemyID", default=None)
    itemID: Optional[List[int]] = Field(alias="itemID", default=None)
    hasItem: Optional[List[int]] = Field(alias="hasItem", default=None)
    objective: Optional[List[int]] = Field(alias="objective", default=None)
    unknown5: Optional[List[int]] = Field(alias="unknown5", default=None)
    unknown6: Optional[List[int]] = Field(alias="unknown6", default=None)
    unknown7: Optional[List[int]] = Field(alias="unknown7", default=None)
    hasPlanet: Optional[List[int]] = Field(alias="hasPlanet", default=None)
    planet: Optional[List[int]] = Field(alias="planet", default=None)


class Task2(BaseApiModel):
    """
    Represents a task in an Assignment that needs to be completed
    to finish the assignment.

    """

    type: Optional[int] = Field(
        alias="type",
        default=None,
        description="A numerical value pertaining to the type of task to be completed."
        + "  Only the Task types the community has seen before are known.",
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
        + " already recieved by the community are known.",
    )

    def taskAdvanced(self) -> Tuple[str, TaskData]:
        """return task type, and model containing task details."""
        typev = int(self.type) if self.type is not None else 0
        task_type = task_types.get(typev, f"Unknown Task Type {typev}")
        taskdata = TaskData()

        for v, vt in zip(self["values"], self["valueTypes"]):
            # print(v, value_types.get(vt, "Unmapped vt"))
            attr_name = value_types[vt]
            if taskdata[attr_name] is None:
                taskdata.set(attr_name, [])
            taskdata[attr_name].append(v)
        return task_type, taskdata

    def task_str(
        self,
        curr_progress: int,
        e: int = 0,
        planets: Dict[int, Planet] = {},
        last_progess=None,
        projected=None,
        show_faction=False,
    ):
        """
        Generate a string representation of the task progress.

        Args:
            curr_progress (int): The current progress of the task.
            e (int, optional): The index or step for this task. Defaults to 0.
            planets (Dict[int, Planet], optional): A dictionary containing planets information. Defaults to {}.
            last_progess (Any, optional): The last recorded progress. Defaults to None.
            projected (Any, optional): Projected future progress. Defaults to None.
            show_faction (bool, optional): Whether or not to show the faction. Defaults to False.

        Returns:
            str: A string containing the task information.
        """
        task_type, taskdata = self.taskAdvanced()
        curr = curr_progress
        taskstr = f"{e}. {task_type}: {hf(curr)}"
        if self.type == 11 or self.type == 13:
            taskstr = self._task_liberate_control(taskstr, taskdata, curr, e, planets)
        elif self.type == 2:
            taskstr = self._task_get_samples(taskstr, taskdata, curr, planets)
        elif self.type == 12:
            taskstr = self._task_defend(taskstr, taskdata, curr, e, planets)
        elif self.type == 3:
            taskstr = self._task_exterminate(taskstr, taskdata, curr, planets, projected)
        elif self.type == 15:
            taskstr = self._task_conquest(taskstr, taskdata, curr, e, planets)
        else:
            taskstr += json.dumps(taskdata.__dict__, default=str)[:258]
        if last_progess:
            taskstr += f"`[change {last_progess}]`"
        return taskstr

    def _task_conquest(
        self,
        taskstr: str,
        taskdata: TaskData,
        curr: int,
        e: int,
        planets: Dict[int, Planet],
    ):
        """
        Handle task string formatting for liberate/control tasks.

        Args:
            taskstr (str): The current task string.
            taskdata (TaskData): Data containing the details of the task.
            curr (int): The current progress of the task.
            e (int): The index or step for this task.
            planets (Dict[int, Planet]): A dictionary containing planet information.

        Returns:
            str: Updated task string with liberate/control details.
        """
        if not taskdata.goal:
            taskstr += json.dumps(taskdata.__dict__, default=str)[:258]
            return taskstr
        faction_name = ""
        if taskdata.faction:
            faction_name = " to " + faction_names.get(
                taskdata.faction[0], f"Unknown Faction {taskdata.faction[0]}"
            )
        goal = taskdata.goal[0]
        taskstr = f"{e}. Conquest.  Liberate more planets than are lost{faction_name} until the order ends. `{curr}/{goal}`"
        taskstr += self._task_display_planet(taskdata, planets)
        return taskstr

    def _task_liberate_control(
        self,
        taskstr: str,
        taskdata: TaskData,
        curr: int,
        e: int,
        planets: Dict[int, Planet],
    ):
        """
        Handle task string formatting for liberate/control tasks.

        Args:
            taskstr (str): The current task string.
            taskdata (TaskData): Data containing the details of the task.
            curr (int): The current progress of the task.
            e (int): The index or step for this task.
            planets (Dict[int, Planet]): A dictionary containing planet information.

        Returns:
            str: Updated task string with liberate/control details.
        """
        if not taskdata.planet:
            taskstr += json.dumps(taskdata.__dict__, default=str)[:108]
            return taskstr
        planet_id = taskdata.planet[0]
        planet_name = "ERR"
        health = "?"
        if int(planet_id) in planets:
            planet = planets[int(planet_id)]
            planet_name = planet.get_name()
            health = planet.health_percent()
        task_mode = "Liberate" if self.type == 11 else "Control"
        taskstr = (
            f"{e}. {task_mode} {planet_name}. Status: `{'ok' if curr == 1 else f'{health},{curr}'}`"
        )
        return taskstr

    def _task_get_samples(
        self, taskstr: str, taskdata: TaskData, curr: int, planets: Dict[int, Planet]
    ):
        """
        Handle task string formatting for "get samples" tasks.

        Args:
            taskstr (str): The current task string.
            taskdata (TaskData): Data containing the details of the task.
            curr (int): The current progress of the task.
            planets (Dict[int, Planet]): A dictionary containing planet information.

        Returns:
            str: Updated task string with sample collection details.
        """
        if not taskdata.goal:
            taskstr += json.dumps(taskdata.__dict__, default=str)[:258]
            return taskstr
        faction_name = ""
        if taskdata.faction:
            faction_name = (
                "("
                + faction_names.get(taskdata.faction[0], f"Unknown Faction {taskdata.faction[0]}")
                + " type)"
            )
        goal = taskdata.goal[0]
        rarity = ""
        if taskdata.itemID:
            rare = taskdata.itemID[0]
            rarity = str(samples.get(rare, rare)) + str(" ")
        taskstr += f"/{hf(goal)} {rarity}samples ({round((int(curr) / int(goal)) * 100.0, 3)}) {faction_name}"
        taskstr += self._task_display_planet(taskdata, planets)
        return taskstr

    def _task_defend(
        self,
        taskstr: str,
        taskdata: TaskData,
        curr: int,
        e: int,
        planets: Dict[int, Planet],
    ):
        """
        Handle task string formatting for defend tasks.

        Args:
            taskstr (str): The current task string.
            taskdata (TaskData): Data containing the details of the task.
            curr (int): The current progress of the task.
            e (int): The index or step for this task.
            planets (Dict[int, Planet]): A dictionary containing planet information.

        Returns:
            str: Updated task string with defense details.
        """
        if not taskdata.goal:
            taskstr += json.dumps(taskdata.__dict__, default=str)[:258]
            return taskstr
        faction_name = ""
        if taskdata.faction:
            faction_name = " from " + faction_names.get(
                taskdata.faction[0], f"Unknown Faction {taskdata.faction[0]}"
            )
        goal = taskdata.goal[0]
        taskstr = f"{e}. Defend {hf(curr)}/{hf(goal)} planets{faction_name}"
        taskstr += self._task_display_planet(taskdata, planets)
        return taskstr

    def _task_display_planet(self, taskdata: TaskData, planets: Dict[int, Planet]):
        taskstr = ""
        if taskdata.hasPlanet and taskdata.planet:
            if not taskdata.hasPlanet[0]:
                return ""
            for ind in taskdata.planet:
                if int(ind) in planets:
                    planet = planets[int(ind)]
                    taskstr += f", On {planet.get_name()}"
        return taskstr

    def _task_exterminate(
        self,
        taskstr: str,
        taskdata: TaskData,
        curr: int,
        planets: Dict[int, Planet],
        projected=None,
    ):
        """
        Handle task string formatting for exterminate tasks.

        Args:
            taskstr (str): The current task string.
            taskdata (TaskData): Data containing the details of the task.
            curr (int): The current progress of the task.
            planets (Dict[int, Planet]): A dictionary containing planet information.
            projected (Any, optional): Projected future progress. Defaults to None.

        Returns:
            str: Updated task string with exterminate details, including projected progress if present.
        """
        if not (taskdata.goal and taskdata.faction):
            taskstr += json.dumps(taskdata.__dict__, default=str)[:258]
            return taskstr
        faction_name = faction_names.get(
            taskdata.faction[0], f"Unknown Faction {taskdata.faction[0]}"
        )
        goal = taskdata.goal[0]
        enemy = ""
        if taskdata.enemyID:
            enemy_id = taskdata.enemyID[0]
            if enemy_id:
                enemy = enemies.get(enemy_id, f"UNKNOWN {enemy_id}")
        percent_done = round((int(curr) / int(goal)) * 100.0, 4)
        taskstr += f"/{hf(goal)} ({percent_done}) {enemy} {faction_name}"
        taskstr += self._task_display_planet(taskdata, planets)
        if projected:
            status = "UNKNOWN"
            if curr > goal:
                status = "VICTORY!"
            elif projected > goal:
                status = "ABOVE QUOTA!"
            elif projected < goal:
                status = "WARNING, UNDER QUOTA!"
            taskstr += f"\n  * Projected Result:`{hf(projected)}`, **{status}**  "
        return taskstr
