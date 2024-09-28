import datetime
from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel

from ..util.utils import (
    human_format as hf,
    select_emoji as emj,
    changeformatif as cfi,
    extract_timestamp as et,
    seconds_to_time_stamp as sts,
)


class Statistics(BaseApiModel):
    """
    Contains statistics of missions, kills, success rate etc for the galaxy as a whole OR a single planet.

    """

    missionsWon: Optional[int] = Field(
        alias="missionsWon", default=None, description="The amount of missions won."
    )

    missionsLost: Optional[int] = Field(
        alias="missionsLost", default=None, description="The amount of missions lost."
    )

    missionTime: Optional[int] = Field(
        alias="missionTime",
        default=None,
        description="The total amount of time spent planetside (in seconds).",
    )

    terminidKills: Optional[int] = Field(
        alias="terminidKills",
        default=None,
        description="The total amount of bugs killed since start of the season.",
    )

    automatonKills: Optional[int] = Field(
        alias="automatonKills",
        default=None,
        description="The total amount of automatons killed since start of the season.",
    )

    illuminateKills: Optional[int] = Field(
        alias="illuminateKills",
        default=None,
        description="The total amount of Illuminate killed since start of the season.",
    )

    bulletsFired: Optional[int] = Field(
        alias="bulletsFired", default=None, description="The total amount of bullets fired"
    )

    bulletsHit: Optional[int] = Field(
        alias="bulletsHit", default=None, description="The total amount of bullets hit"
    )

    timePlayed: Optional[int] = Field(
        alias="timePlayed",
        default=None,
        description="The total amount of time played (including off-planet) in seconds.",
    )

    deaths: Optional[int] = Field(
        alias="deaths",
        default=None,
        description="The amount of casualties on the side of humanity.",
    )

    revives: Optional[int] = Field(
        alias="revives", default=None, description="The amount of revives(?)."
    )

    friendlies: Optional[int] = Field(
        alias="friendlies", default=None, description="The amount of friendly fire casualties."
    )

    missionSuccessRate: Optional[int] = Field(
        alias="missionSuccessRate",
        default=None,
        description="A percentage indicating how many started missions end in success.",
    )

    accuracy: Optional[int] = Field(
        alias="accuracy",
        default=None,
        description="A percentage indicating average accuracy of Helldivers.",
    )

    playerCount: Optional[int] = Field(
        alias="playerCount",
        default=None,
        description="The total amount of players present (at the time of the snapshot).",
    )

    def __sub__(self, other: "Statistics") -> "Statistics":
        sub = Statistics(
            missionsWon=(self.missionsWon or 0) - (other.missionsWon or 0),
            missionsLost=(self.missionsLost or 0) - (other.missionsLost or 0),
            missionTime=(self.missionTime or 0) - (other.missionTime or 0),
            terminidKills=(self.terminidKills or 0) - (other.terminidKills or 0),
            automatonKills=(self.automatonKills or 0) - (other.automatonKills or 0),
            illuminateKills=(self.illuminateKills or 0) - (other.illuminateKills or 0),
            bulletsFired=(self.bulletsFired or 0) - (other.bulletsFired or 0),
            bulletsHit=(self.bulletsHit or 0) - (other.bulletsHit or 0),
            timePlayed=(self.timePlayed or 0) - (other.timePlayed or 0),
            deaths=(self.deaths or 0) - (other.deaths or 0),
            revives=(self.revives or 0) - (other.revives or 0),
            friendlies=(self.friendlies or 0) - (other.friendlies or 0),
            missionSuccessRate=(self.missionSuccessRate or 0) - (other.missionSuccessRate or 0),
            accuracy=(self.accuracy or 0) - (other.accuracy or 0),
            playerCount=(self.playerCount or 0) - (other.playerCount or 0),
            time_delta=self.retrieved_at - other.retrieved_at,  # type: ignore
        )
        return sub

    @staticmethod
    def average(stats_list: List["Statistics"]) -> "Statistics":
        """
        Average together a list of calculated Statistic Deltas.

        """
        count = len(stats_list)
        if count == 0:
            return Statistics()

        avg_time = (
            sum(
                stats.time_delta.total_seconds()
                for stats in stats_list
                if stats.time_delta is not None
            )
            // count
        )
        avg_stats = Statistics(
            missionsWon=sum(stat.missionsWon for stat in stats_list if stat.missionsWon is not None)
            // count,
            missionsLost=sum(
                stat.missionsLost for stat in stats_list if stat.missionsLost is not None
            )
            // count,
            missionTime=sum(stat.missionTime for stat in stats_list if stat.missionTime is not None)
            // count,
            terminidKills=sum(
                stat.terminidKills for stat in stats_list if stat.terminidKills is not None
            )
            // count,
            automatonKills=sum(
                stat.automatonKills for stat in stats_list if stat.automatonKills is not None
            )
            // count,
            illuminateKills=sum(
                stat.illuminateKills for stat in stats_list if stat.illuminateKills is not None
            )
            // count,
            bulletsFired=sum(
                stat.bulletsFired for stat in stats_list if stat.bulletsFired is not None
            )
            // count,
            bulletsHit=sum(stat.bulletsHit for stat in stats_list if stat.bulletsHit is not None)
            // count,
            timePlayed=sum(stat.timePlayed for stat in stats_list if stat.timePlayed is not None)
            // count,
            deaths=sum(stat.deaths for stat in stats_list if stat.deaths is not None) // count,
            revives=sum(stat.revives for stat in stats_list if stat.revives is not None) // count,
            friendlies=sum(stat.friendlies for stat in stats_list if stat.friendlies is not None)
            // count,
            missionSuccessRate=sum(
                stat.missionSuccessRate
                for stat in stats_list
                if stat.missionSuccessRate is not None
            )
            // count,
            accuracy=sum(stat.accuracy for stat in stats_list if stat.accuracy is not None)
            // count,
            playerCount=sum(stat.playerCount for stat in stats_list if stat.playerCount is not None)
            // count,
            time_delta=datetime.timedelta(seconds=avg_time),
        )

        return avg_stats

    def format_statistics(self) -> str:
        """
        Return statistics formatted in a nice string.
        """
        mission_stats = f"W:{hf(self.missionsWon)},"
        mission_stats += f"L:{hf(self.missionsLost)}"
        missiontime = f"Time:{sts(self.missionTime)} sec"

        # Format kill statistics
        kill_stats = (
            f"T:{hf(self.terminidKills)}, " f"A:{hf(self.automatonKills)}, " f"DATA EXPUNGED"
        )
        #             f"I: {hf(self.illuminateKills)}"

        # Format deaths and friendlies statistics
        deaths_and_friendlies = f"Deaths/Friendlies: {hf(self.deaths)}/" f"{hf(self.friendlies)}"

        # Format player count
        player_count = f"{emj('hdi')}: {hf(self.playerCount)}"
        thistime = round(max(self.missionTime, 1) / max((self.missionsWon + self.missionsLost), 1), 4)  # type: ignore

        mission_stats += f"\n Time per mission: {sts(thistime)}"
        # Concatenate all formatted statistics
        statsa = f"`[Missions: {mission_stats}]`\n`[{missiontime}]`\n`[Kills: {kill_stats}]`"
        statsb = f"`[{deaths_and_friendlies}]`"
        statsc = f"`Total Time: {sts(self.timePlayed)}`"
        return f"{player_count}\n{statsa}\n{statsb}\n{statsc}"

    def diff_format(self, other: "Statistics") -> str:
        """
        Returns statistics formatted in a nice string with difference from another Statistics class.

        Args:
            other (Statistics): The other Statistics instance to compare with.

        Returns:
            str: Formatted statistics with differences.
        """
        # Calculate differences for each statistic

        # Format each statistic with its difference
        missiontotal = max(1, self.missionsWon + self.missionsLost)  # type: ignore
        misiontotalother = max(1, other.missionsWon + other.missionsLost)  # type: ignore
        mission_stats = f"W:{hf(self.missionsWon)} ({other.missionsWon}),"
        mission_stats += f"L:{hf(self.missionsLost)} ({other.missionsLost})"
        mission_stats += f"{round(100.0*(other.missionsWon/(max(other.missionsWon+other.missionsLost,1))),1)}"  # type: ignore
        mission_stats += f"\nTime:{sts(self.missionTime)}({sts(other.missionTime)})"

        thistime = round(max(self.missionTime, 1) / (missiontotal), 4)
        lasttime = round(max(other.missionTime, 1) / (misiontotalother), 4)
        mission_stats += f"\n Time per mission: {sts(thistime)}({sts(lasttime)})"
        kill_stats = f"T:{hf(self.terminidKills)} ({other.terminidKills}),"
        kill_stats += f"A:{hf(self.automatonKills)} ({other.automatonKills}),"
        kill_stats += "DATA EXPUNGED"
        bullets_stats = f"Bullets Hit/Fired: {hf(self.bulletsHit)}/{hf(self.bulletsFired)} ({other.bulletsHit}/{other.bulletsFired})"
        deaths_and_friendlies = f"Deaths/Friendlies: {hf(self.deaths)}/{hf(self.friendlies)} ({other.deaths}/{other.friendlies})"

        player_count = f"{emj('hdi')}: {hf(self.playerCount)} ({other.playerCount})"

        # Concatenate all formatted statistics
        statsa = f"`[Missions: {mission_stats}]`\n `[Kills: {kill_stats}]`\n`[{bullets_stats}]`"
        statsb = f"`[{deaths_and_friendlies}]`"
        statsc = f"`Total Time: {sts(self.timePlayed)}({sts(other.timePlayed)})`"
        return f"{player_count}\n{statsa}\n{statsb}\n{statsc}"
