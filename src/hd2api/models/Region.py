import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field

from ..util.utils import changeformatif as cfi
from ..util.utils import extract_timestamp as et
from ..util.utils import format_datetime as fdt
from ..util.utils import select_emoji as emj
from .ABC.model import BaseApiModel, HealthMixin

from ..constants import faction_names, region_size_enums


class Region(BaseApiModel, HealthMixin):
    """
    Combined model representing both dynamic and static information
    about a region on a planet, using data from PlanetRegion and PlanetRegionInfo.
    """

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=None,
        description="The numerical identifier for the planet.",
    )
    # From PlanetRegionInfo (static/config)
    keyCombo: str = Field(
        alias="keyCombo",
        default="NOKEY",
        description="Unique key of planetIndex_regionIndex",
    )
    id: Optional[int] = Field(
        alias="id",
        default=None,
        description="The identifier of this campaign, hash of key_combo.",
    )
    # From PlanetRegionInfo (static/config)
    planetName: Optional[str] = Field(
        alias="planetName", default=None, description="The name for the planet."
    )

    regionIndex: Optional[int] = Field(
        alias="regionIndex",
        default=None,
        description="The numerical identifier for the region within the planet.",
    )

    settingsHash: Optional[int] = Field(
        alias="settingsHash",
        default=None,
        description="Hash for the internal region settings.",
    )

    hash: Optional[int] = Field(
        alias="hash",
        default=None,
        description="Hash for the internal region settings.",
    )

    name: Optional[str] = Field(
        alias="name", default=None, description="The name of the region."
    )

    description: Optional[str] = Field(
        alias="description",
        default=None,
        description="A brief description of the region.",
    )

    maxHealth: Optional[int] = Field(
        alias="maxHealth",
        default=None,
        description="Total health needed for liberation or full control.",
    )

    regionSize: Optional[Union[int, str]] = Field(
        alias="regionSize",
        default=None,
        description="Size or scale factor for the region.",
    )
    size: Optional[Union[int, str]] = Field(
        alias="size",
        default=None,
        description="Size or scale factor for the region.",
    )

    # From PlanetRegion (dynamic/state)
    owner: Optional[Union[int, str]] = Field(
        alias="owner",
        default=None,
        description="The faction currently controlling the region.",
    )

    health: Optional[int] = Field(
        alias="health", default=None, description="Current health of the region."
    )

    regenPerSecond: Optional[float] = Field(
        alias="regenPerSecond",
        default=None,
        description="Health regeneration per second.",
    )

    availabilityFactor: Optional[float] = Field(
        alias="availabilityFactor",
        default=None,
        description="A factor indicating the availability of the region.",
    )

    isAvailable: Optional[bool] = Field(
        alias="isAvailable",
        default=None,
        description="Whether the region is currently available for missions.",
    )

    players: Optional[int] = Field(
        alias="players",
        default=None,
        description="Number of active players in the region.",
    )

    def __sub__(self, other: "Region") -> "Region":
        """
        Compute the difference between two Region objects.
        """
        health_diff = (
            self.health - other.health
            if self.health is not None and other.health is not None
            else None
        )

        players_diff = (
            self.players - other.players
            if self.players is not None and other.players is not None
            else None
        )

        return Region(
            planetIndex=self.planetIndex,
            regionIndex=self.regionIndex,
            name=self.name,
            description=self.description,
            settingsHash=self.settingsHash,
            hash=self.hash,
            id=self.id,
            maxHealth=self.maxHealth,
            regionSize=self.regionSize,
            size=self.size,
            owner=self.owner,
            health=health_diff,
            regenPerSecond=self.regenPerSecond,
            availabilityFactor=self.availabilityFactor,
            isAvailable=self.isAvailable,
            players=players_diff,
            retrieved_at=self.retrieved_at,
            time_delta=self.retrieved_at - other.retrieved_at,  # type: ignore
        )

    def calculate_change(self, diff: "Region") -> float:
        if not diff.time_delta or diff.time_delta.total_seconds() == 0:
            return 0.0
        return diff.health / diff.time_delta.total_seconds()

    def simple_region_view(
        self, prev: Optional["Region"] = None, avg: Optional["Region"] = None
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

        name = f"P#{self.planetIndex}:{self.planetName}-{self.name}"
        players = f"{emj('hdi')}: `{self.players} {cfi(diff.players)}`"

        outlist = [
            self.description,
            f"{players}, Owner: {self.owner}\n Is Available {self.isAvailable}",
        ]
        outlist.append(f"Availability Factor: {self.availabilityFactor}")
        outlist.append(f"Region Size: {self.size}")

        outlist.append(
            f"HP: {self.get_health_percent(self.health)}%({self.health}) {cfi(self.get_health_percent(diff.health))}`"
        )
        outlist.append(
            f"Regen:`{self.regenPerSecond}, {round((100 * (self.regenPerSecond / self.maxHealth)) * 60 * 60, 2)}%`"  # type: ignore
        )  # type: ignore
        if avg:
            remaining_time = self.estimate_remaining_lib_time(avg)
            if remaining_time:
                outlist.append(remaining_time)

        return name, outlist

    def inline_view(self):
        if self.isAvailable:
            outp = f"{round((self.health / max(self.maxHealth, 1)) * 100, 1)}%"

            return f"[{self.size} {self.name}-{outp}]"
        else:
            fact = self.owner
            if isinstance(self.owner, int):
                fact = faction_names.get(int(fact), str(fact))
            return f"[{self.size} {self.name}-{fact}]"

    def calculate_timeval(self, change: float, is_positive: bool) -> datetime.datetime:
        if self.health is None or self.maxHealth is None:
            return self.retrieved_at

        if is_positive:
            seconds = abs((self.maxHealth - self.health) / change)
        else:
            seconds = abs(self.health / change)
        return self.retrieved_at + datetime.timedelta(seconds=seconds)

    def format_estimated_time_string(
        self, change: float, esttime: datetime.datetime
    ) -> str:
        change_str = f"{round(change, 5)}"
        timeval_str = (
            f"Est.Loss {fdt(esttime, 'R')}" if change > 0 else f"{fdt(esttime, 'R')}"
        )
        return f"`[{change_str} dps]`, {timeval_str}"

    def estimate_remaining_lib_time(self, diff: "Region") -> str:
        if not diff.time_delta or diff.time_delta.total_seconds() == 0:
            return ""

        change = self.calculate_change(diff)
        if change == 0:
            return "Stalemate."

        timeval = self.calculate_timeval(change, change > 0)
        return self.format_estimated_time_string(change, timeval)

    @staticmethod
    def average(regions: List["Region"]) -> "Region":
        count = len(regions)
        if count == 0:
            return Region()

        avg_health = sum(r.health for r in regions if r.health is not None) // count
        avg_players = sum(r.players for r in regions if r.players is not None) // count
        avg_time = (
            sum(r.time_delta.total_seconds() for r in regions if r.time_delta) // count
        )

        return Region(
            planetIndex=regions[0].planetIndex,
            regionIndex=regions[0].regionIndex,
            name=regions[0].name,
            description=regions[0].description,
            settingsHash=regions[0].settingsHash,
            maxHealth=regions[0].maxHealth,
            regionSize=regions[0].regionSize,
            owner=regions[0].owner,
            health=avg_health,
            players=avg_players,
            regenPerSecond=regions[0].regenPerSecond,
            availabilityFactor=regions[0].availabilityFactor,
            isAvailable=regions[0].isAvailable,
            retrieved_at=regions[0].retrieved_at,
            time_delta=datetime.timedelta(seconds=avg_time),
        )
