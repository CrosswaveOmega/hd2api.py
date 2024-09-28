import datetime
from typing import *

import json

from pydantic import Field
from .ABC.model import BaseApiModel, HealthMixin

from .Biome import Biome
from .Event import Event
from .Hazard import Hazard
from .Position import Position
from .Statistics import Statistics
from .Effects import KnownPlanetEffect
from ..util.utils import (
    human_format as hf,
    select_emoji as emj,
    changeformatif as cfi,
    extract_timestamp as et,
    format_datetime as fdt,
)
from .Base.PlanetStatus import PlanetStatus


class Planet(BaseApiModel, HealthMixin):
    """
    All aggregated information the community has on a planet.
    Combines PlanetStatus, PlanetInfo, PlanetStats, and the
    static information from the statics/planets files

    """

    index: Optional[int] = Field(
        alias="index",
        default=None,
        description="The unique identifier ArrowHead assigned to this planet.",
    )

    name: Optional[Union[str, Dict[str, Any]]] = Field(
        alias="name", default=None, description="The name of the planet, as shown in game."
    )

    sector: Optional[str] = Field(
        alias="sector",
        default=None,
        description="The name of the sector the planet is in, as shown in game.",
    )

    sector_id: Optional[int] = Field(
        alias="sector_id",
        default=None,
        description="The identifier of the sector this planet is located in as returned from planet info.  For reasons unknown, it does not always match up with the .",
    )

    biome: Optional[Biome] = Field(
        alias="biome", default=None, description="The biome this planet has."
    )

    hazards: Optional[List[Optional[Hazard]]] = Field(
        alias="hazards", default=None, description="All Hazards that are applicable to this planet."
    )

    hash: Optional[int] = Field(
        alias="hash",
        default=None,
        description="A hash assigned to the planet pointing to the internal planet settings for this world.",
    )

    position: Optional[Position] = Field(
        alias="position",
        default=None,
        description="The coordinates of this planet on the galactic war map.",
    )

    waypoints: Optional[List[int]] = Field(
        alias="waypoints",
        default=None,
        description="A list of Index of all the planets to which this planet is connected.",
    )

    maxHealth: Optional[int] = Field(
        alias="maxHealth", default=None, description="The maximum health pool of this planet."
    )

    health: Optional[int] = Field(
        alias="health", default=None, description="The current planet this planet has."
    )

    disabled: Optional[bool] = Field(
        alias="disabled",
        default=None,
        description="Whether or not this planet is disabled, as assigned by ArrowHead.",
    )

    initialOwner: Optional[str] = Field(
        alias="initialOwner",
        default=None,
        description="The faction that originally owned the planet.",
    )

    currentOwner: Optional[str] = Field(
        alias="currentOwner",
        default=None,
        description="The faction that currently controls the planet.",
    )

    regenPerSecond: Optional[float] = Field(
        alias="regenPerSecond",
        default=None,
        description="How much the planet regenerates per second if left alone.",
    )

    event: Optional[Event] = Field(
        alias="event",
        default=None,
        description="Information on the active event ongoing on this planet, if one is active.",
    )

    statistics: Optional[Statistics] = Field(
        alias="statistics", default=None, description="A set of statistics scoped to this planet."
    )

    attacking: Optional[List[int]] = Field(
        alias="attacking",
        default=None,
        description="A list of Index integers that this planet is currently attacking.",
    )
    activePlanetEffects: Optional[List[KnownPlanetEffect]] = Field(
        alias="activePlanetEffects",
        default=None,
        description="List of any active planet effects that happen to be assigned to this planet, such as the black hole in the place of Meridia",
    )

    def __sub__(self, other: "Planet") -> "Planet":
        """
        Subtract values from another planet.
        """
        # Calculate the values for health, statistics, and event based on subtraction
        new_health = (
            self.health - other.health
            if self.health is not None and other.health is not None
            else None
        )
        if self.statistics is not None and other.statistics is not None:
            new_statistics = self.statistics - other.statistics
        else:
            new_statistics = None

        new_event = (
            self.event - other.event
            if self.event is not None and other.event is not None
            else self.event
        )

        # Create a new instance of the Planet class with calculated values
        planet = Planet(
            health=new_health,
            statistics=new_statistics,
            event=new_event,
            index=self.index,
            name=self.name,
            sector=self.sector,
            biome=self.biome,
            hazards=self.hazards,
            hash=self.hash,
            position=self.position,
            waypoints=self.waypoints,
            maxHealth=self.maxHealth,
            disabled=self.disabled,
            initialOwner=self.initialOwner,
            currentOwner=self.currentOwner,
            regenPerSecond=self.regenPerSecond,
            attacking=self.attacking,
            time_delta=self.retrieved_at - other.retrieved_at,  # type: ignore
        )
        return planet

    def calculate_change(self, diff: "Planet") -> float:
        """
        Calculate the rate of change in health over time.

        Args:
            diff (Planet): A Planet object representing the difference in health and time.

        Returns:
            float: The rate of change in health per second.
        """
        time_elapsed = diff.time_delta
        if time_elapsed.total_seconds() == 0:
            return 0.0
        return diff.health / time_elapsed.total_seconds()

    def calculate_timeval(self, change: float, is_positive: bool) -> datetime.datetime:
        """
        Calculate the future datetime when the planet's health will reach the maxHealth or zero.

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
        change_str = f"{round(change, 5)}"
        timeval_str = f"Est.Loss {fdt(esttime,'R')}" if change > 0 else f"{fdt(esttime,'R')}"

        return f"`[{change_str} dps]`, {timeval_str}"

    def estimate_remaining_lib_time(self, diff: "Planet") -> str:
        """
        Estimate the remaining life time of the planet based on the current rate of health change.

        Args:
            diff (Planet): A Planet object with difference in health and time.

        Returns:
            str: A string representation of the rate of change and the estimated time of loss or gain.
        """
        time_elapsed = diff.time_delta
        if time_elapsed.total_seconds() == 0:
            return ""

        change = self.calculate_change(diff)
        if change == 0:
            if self.currentOwner.lower() != "humans":
                return "Stalemate."
            return ""

        timeval = self.calculate_timeval(change, change > 0)

        return self.format_estimated_time_string(change, timeval)

    def get_name(self, faction=True) -> str:
        """Get the name of the planet, along with occupying faction
        and planet index."""
        if not faction:
            return f"P#{self.index}: {self.name}"
        faction = emj(self.currentOwner.lower())
        return f"{faction}P#{self.index}: {self.name}"

    @staticmethod
    def average(planets_list: List["Planet"]) -> "Planet":
        """Average together a list of planet differences over time."""
        count = len(planets_list)
        if count == 0:
            return Planet()

        avg_health = (
            sum(planet.health for planet in planets_list if planet.health is not None) // count
        )

        stats = []
        for planet in planets_list:
            if planet.statistics is not None:
                stats.append(planet.statistics)

        avg_statistics = Statistics.average(stats)
        print("avgstat", avg_statistics)
        avg_event = Event.average(
            [planet.event for planet in planets_list if planet.event is not None]
        )

        avg_time = (
            sum(
                planet.time_delta.total_seconds()
                for planet in planets_list
                if planet.time_delta is not None
            )
            // count
        )
        avg_planet = Planet(
            health=avg_health,
            statistics=avg_statistics,
            event=avg_event,
            index=planets_list[0].index,
            name=planets_list[0].name,
            sector=planets_list[0].sector,
            hash=planets_list[0].hash,
            waypoints=planets_list[0].waypoints,
            maxHealth=planets_list[0].maxHealth,
            disabled=planets_list[0].disabled,
            initialOwner=planets_list[0].initialOwner,
            currentOwner=planets_list[0].currentOwner,
            regenPerSecond=planets_list[0].regenPerSecond,
            attacking=planets_list[0].attacking,
            time_delta=datetime.timedelta(seconds=avg_time),
        )
        # avg_planet.time_delta = datetime.timedelta(seconds=avg_time)
        return avg_planet

    def campaign_against(self) -> str:
        """Get the emoji of the faction that is occupying or defending this planet."""
        faction = emj(self.currentOwner.lower())
        if self.event:
            evt = self.event
            return emj(self.event.faction.lower())
        return faction

    def simple_planet_view(
        self,
        prev: Optional["Planet"] = None,
        avg: Optional["Planet"] = None,
        show_hp_without_event: bool = True,
    ) -> Tuple[str, List[str]]:
        """Return a string containing the formated state of the planet.

        Args:
            prev (Optional[&#39;Planet&#39;], optional):
            avg (Optional[&#39;Planet&#39;], optional):Average stats for the past X planets

        Returns:
            Tuple[str,str]: _description_
        """
        diff = self - self
        if prev is not None:
            diff = prev

        faction = emj(self.currentOwner.lower())

        name = f"{faction}P#{self.index}: {self.name}"
        players = (
            f"{emj('hdi')}: `{self.statistics.playerCount} {cfi(diff.statistics.playerCount)}`"
        )
        outlist = [f"{players}"]
        if (not self.event) or show_hp_without_event:
            outlist.append(
                f"HP `{self.get_health_percent(self.health)}% {cfi(self.get_health_percent(diff.health))}`"
            )
            outlist.append(f"Decay:`{round((100*(self.regenPerSecond/self.maxHealth))*60*60,2)}`")  # type: ignore
        if avg:
            remaining_time = self.estimate_remaining_lib_time(avg)
            if remaining_time:
                outlist.append(remaining_time)
        if self.event:
            evt = self.event
            timev = fdt(et(evt.endTime), "R")
            event_fact = emj(self.event.faction.lower())
            # , {evt.health}{cfi(diff.event.health)}/{evt.maxHealth}.
            outlist.append(f"Defend from {event_fact}")
            outlist.append(
                f"EventHP:{evt.get_health_percent(evt.health)}% {cfi(evt.get_health_percent(diff.event.health))}"
            )
            outlist.append(f"Deadline: [{timev}]")
            if avg:
                if avg.event:
                    outlist.append(f"{self.event.estimate_remaining_lib_time(avg.event)}")

        return name, outlist
