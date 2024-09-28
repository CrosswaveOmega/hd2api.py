from typing import *
import datetime
from pydantic import Field
from .ABC.model import BaseApiModel, HealthMixin
import logging

from ..util.utils import (
    human_format as hf,
    select_emoji as emj,
    changeformatif as cfi,
    extract_timestamp as et,
    format_datetime as fdt,
)


hd2api_logger = logging.getLogger("hd2api_logger")


class Event(BaseApiModel, HealthMixin):
    """
    None model
        An ongoing event on a Planet.

    """

    id: Optional[int] = Field(
        alias="id", default=None, description="The unique identifier of this event."
    )

    eventType: Optional[int] = Field(
        alias="eventType", default=None, description="The type of event."
    )

    faction: Optional[str] = Field(
        alias="faction", default=None, description="The faction that initiated the event."
    )

    health: Optional[int] = Field(
        alias="health", default=None, description="The health of the Event at the time of snapshot."
    )

    maxHealth: Optional[int] = Field(
        alias="maxHealth",
        default=None,
        description="The maximum health of the Event at the time of snapshot.",
    )

    startTime: Optional[str] = Field(
        alias="startTime",
        default=None,
        description="Datetime for the event was roughly started, based on wartime.",
    )

    endTime: Optional[str] = Field(
        alias="endTime",
        default=None,
        description="Datetime for when the event will roughly end, based on wartime.",
    )

    campaignId: Optional[int] = Field(
        alias="campaignId",
        default=None,
        description="The identifier for a Campaign linked to this event.",
    )

    jointOperationIds: Optional[List[int]] = Field(
        alias="jointOperationIds",
        default=None,
        description="A list of joint operation identifiers linked to this event.",
    )

    def __sub__(self, other: "Event") -> "Event":
        new_health = (
            self.health - other.health
            if self.health is not None and other.health is not None
            else None
        )
        event = Event(
            id=self.id,
            eventType=self.eventType,
            faction=self.faction,
            health=new_health,
            maxHealth=self.maxHealth,
            startTime=self.startTime,
            endTime=self.endTime,
            campaignId=self.campaignId,
            jointOperationIds=self.jointOperationIds,
            time_delta=self.retrieved_at - other.retrieved_at,  # type: ignore
        )
        return event

    @staticmethod
    def average(events_list: List["Event"]) -> "Event":
        count = len(events_list)
        if count == 0:
            return Event()

        avg_health = sum(event.health for event in events_list if event.health is not None) // count
        avg_time = (
            sum(
                event.time_delta.total_seconds()
                for event in events_list
                if event.time_delta is not None and isinstance(event.time_delta, datetime.timedelta)
            )
            // count
        )
        avg_event = Event(
            health=avg_health,
            maxHealth=events_list[0].maxHealth,
            faction=events_list[0].faction,
            startTime=events_list[0].startTime,
            endTime=events_list[0].endTime,
            eventType=events_list[0].eventType,
            id=events_list[0].id,
            campaignId=events_list[0].campaignId,
            jointOperationIds=events_list[0].jointOperationIds,
        )
        avg_event.time_delta = datetime.timedelta(seconds=avg_time)
        return avg_event

    def calculate_change(self, diff: "Event") -> float:
        """
        Calculate the rate of change in health over time.

        Args:
            diff (Event): A Event object with the average health change and seconds

        Returns:
            float: The rate of change in health per second.
        """
        time_elapsed = diff.time_delta
        hd2api_logger.info("%d, %s", diff.health, diff.time_delta)
        if time_elapsed.total_seconds() == 0:
            return 0.0
        return diff.health / time_elapsed.total_seconds()

    def calculate_timeval(self, change: float, is_positive: bool) -> datetime.datetime:
        """
        Calculate the future datetime when the events's health will reach the maxHealth or zero.

        Args:
            change (float): The rate of change in health per second.
            is_positive (bool): A boolean indicating if the change is positive or negative.

        Returns:
            datetime: The estimated future datetime.
        """
        if is_positive:
            estimated_seconds = abs((self.maxHealth - self.health) / change)  # type: ignore
        else:
            estimated_seconds = abs(self.health / change)
        return self.retrieved_at + datetime.timedelta(seconds=estimated_seconds)

    def format_estimated_time_string(self, change: float, esttime: datetime.datetime):
        """
        Format the string representing the estimated time and rate of health change.

        Args:
            change (float): The rate of change in health per second.
            esttime (datetime): The estimated datetime when the event's health will reach the threshold.

        Returns:
            str: A formatted string with the change rate and estimated time.
        """
        change_str = f"{round(change, 5)}"
        timeval_str = f"Est.Loss {fdt(esttime,'R')}" if change > 0 else f"Clear {fdt(esttime,'R')}"

        return f"`[{change_str} dps]`, {timeval_str}"

    def estimate_remaining_lib_time(self, diff: "Event") -> str:
        """
        Estimate the remaining life time of the event based on the current rate of health change.

        Args:
            diff (Event):  A Event object with the average health change and timedelta.

        Returns:
            str: A string representation of the rate of change and the estimated time of loss or gain.
        """
        time_elapsed = diff.time_delta

        if not isinstance(time_elapsed, datetime.timedelta):
            hd2api_logger.info("No time elapsed?")
            return ""
        if time_elapsed.total_seconds() == 0:
            return "?"
        change = self.calculate_change(diff)
        if change == 0:
            hd2api_logger.info("No change?")
            return ""

        timeval = self.calculate_timeval(change, change > 0)

        return self.format_estimated_time_string(change, timeval)

    def get_name(self) -> str:
        """Get the id of the event, along with occupying faction and type."""

        event_fact = emj(self.faction.lower())
        return f"{event_fact} Event#{self.id},Type#{self.eventType}:"

    def long_event_details(self, diff: Optional["Event"] = None):
        joint_ops = ", ".join(map(str, self.jointOperationIds))  # type: ignore
        event_details = (
            f"ID: {self.id}, Type: {hf(self.eventType)}, Faction: {self.faction}\n"
            f"Event Health: `{(self.health)}/{(self.maxHealth)}` (`{diff.health if diff is not None else 0}` change)\n"
            f"Start Time: {fdt(et(self.startTime),'R')}, End Time: {fdt(et(self.endTime),'R')}\n"
            f"Campaign ID: {hf(self.campaignId)}, Joint Operation IDs: {joint_ops}"
        )
        return event_details
