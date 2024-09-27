from typing import *

from ..models import *
import datetime as dt


def statistics_builder(
    stats: Union[PlanetStats, GalaxyStats], players: int, retrieved_at: Optional[dt.datetime] = None
) -> Statistics:
    """
    Build a Statistics object.

    Args:
        stats (Union[PlanetStats, GalaxyStats]): Raw object containing statistics data for either a planet or galaxy.
        players (int): The number of players involved.
        retrieved_at (Optional[dt]): The time at which the statistics were retrieved. If not provided, the time will be taken from the stats object.

    Returns:
        Statistics: A Statistics object with the compiled data.
    """
    use_time = retrieved_at
    if not retrieved_at:
        use_time = stats.retrieved_at
    stats_new = Statistics(
        retrieved_at=use_time,
        playerCount=players,
        missionsWon=stats.missionsWon,
        missionsLost=stats.missionsLost,
        missionTime=stats.missionTime,
        terminidKills=stats.bugKills,
        automatonKills=stats.automatonKills,
        illuminateKills=stats.illuminateKills,
        bulletsFired=stats.bulletsFired,
        bulletsHit=stats.bulletsHit,
        timePlayed=stats.timePlayed,
        deaths=stats.deaths,
        revives=stats.revives,
        friendlies=stats.friendlies,
        missionSuccessRate=stats.missionSuccessRate,
        accuracy=stats.accurracy,
    )
    return stats_new
