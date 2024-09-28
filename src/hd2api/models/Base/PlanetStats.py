from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


class PlanetStats(BaseApiModel):
    """
    Raw model similar to GalaxyStats, but scoped to a specific planet.

    """

    planetIndex: Optional[int] = Field(
        alias="planetIndex",
        default=0,
        description="The planetIndex for the planet these stats where gathered from.",
    )

    missionsWon: Optional[int] = Field(
        alias="missionsWon", default=0, description="The amount of missions won."
    )

    missionsLost: Optional[int] = Field(
        alias="missionsLost", default=0, description="The amount of missions lost."
    )

    missionTime: Optional[int] = Field(
        alias="missionTime",
        default=0,
        description="The total amount of time spent planetside (in seconds).",
    )

    bugKills: Optional[int] = Field(
        alias="bugKills",
        default=0,
        description="The total amount of bugs killed since start of the season.",
    )

    automatonKills: Optional[int] = Field(
        alias="automatonKills",
        default=0,
        description="The total amount of automatons killed since start of the season.",
    )

    illuminateKills: Optional[int] = Field(
        alias="illuminateKills",
        default=0,
        description="The total amount of Illuminate killed since start of the season.",
    )

    bulletsFired: Optional[int] = Field(
        alias="bulletsFired", default=0, description="The total amount of bullets fired"
    )

    bulletsHit: Optional[int] = Field(
        alias="bulletsHit", default=0, description="The total amount of bullets hit"
    )

    timePlayed: Optional[int] = Field(
        alias="timePlayed",
        default=0,
        description="The total amount of time played (including off-planet) in seconds.",
    )

    deaths: Optional[int] = Field(
        alias="deaths", default=0, description="The amount of casualties on the side of humanity."
    )

    revives: Optional[int] = Field(
        alias="revives", default=0, description="The amount of revives(?)."
    )

    friendlies: Optional[int] = Field(
        alias="friendlies", default=0, description="The amount of friendly fire casualties."
    )

    missionSuccessRate: Optional[int] = Field(
        alias="missionSuccessRate",
        default=0,
        description="A percentage indicating how many started missions end in success.",
    )

    accurracy: Optional[int] = Field(
        alias="accurracy",
        default=0,
        description="A percentage indicating average accuracy of Helldivers.",
    )
