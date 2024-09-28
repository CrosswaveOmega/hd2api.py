from typing import List, Optional, Type, TypeVar, Dict

import httpx

import datetime as dt
from ..api_config import APIConfig, HTTPException
from ..models import *
from ..models.ABC.model import BaseApiModel

from ..constants import task_types, value_types, faction_names, samples

from .effect_builder import build_planet_effect

from .planet_builder import get_time
from .statistics_builder import statistics_builder


def build_war(diveharder: DiveharderAll) -> War:
    info = diveharder.war_info
    stats = diveharder.planet_stats.galaxy_stats

    player_count = sum(
        st.players for st in diveharder.status.planetStatus if st.players is not None
    )

    stats_build = statistics_builder(stats, player_count)
    war = War(
        retrieved_at=diveharder.status.retrieved_at,
        warId=diveharder.status.warId,
        started=(dt.datetime.fromtimestamp(info.startDate, tz=dt.timezone.utc)).isoformat(),
        ended=(dt.datetime.fromtimestamp(info.endDate, tz=dt.timezone.utc)).isoformat(),
        clientVersion=info.minimumClientVersion,
        now=info.retrieved_at.isoformat(),
        impactMultiplier=diveharder.status.impactMultiplier,
        factions=["Humans", "Terminids", "Automaton", "Illuminate"],
        statistics=stats_build,
    )
    return war
