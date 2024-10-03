from typing import List, Optional, Type, TypeVar, Dict

import httpx

import datetime as dt
from ..api_config import APIConfig, HTTPException
from ..models import *
from ..models.ABC.model import BaseApiModel

from ..constants import task_types, value_types, faction_names, samples

from .effect_builder import build_planet_effect
from .statistics_builder import statistics_builder


def build_planet_basic(
    gstatic: GalaxyStatic,
    index: int,
    planetStatus: PlanetStatus,
    planetInfo: PlanetInfo,
    stats: PlanetStats,
) -> Planet:
    """
    Builds a new Planet object using the provided GalaxyStatic,
    PlanetStatus, PlanetInfo, and PlanetStats fields.

    Args:
        gstatic (GalaxyStatic): The static information about planets, enviornmental effects, and biomes
            in the galaxy
        index (int): Index of the planet within the galaxy.
        planetStatus (PlanetStatus): The Raw PlanetStatus object with a matching index.
        planetInfo (PlanetInfo): The raw PlanetInfo object with a matching index
        stats (PlanetStats): The Game Statistics for the planet.

    Returns:
        Planet: The newly constructed Planet object or None if the planet
        doesn't exist in the provided galaxy static information.
    """
    planet_base = gstatic.planets.get(index, None)
    if not planet_base:
        return None
    biome = gstatic.biomes.get(planet_base.biome, None)  # type: ignore
    env = [gstatic.environmentals.get(e, None) for e in planet_base.environmentals]
    # Build Statistics
    stats_new = statistics_builder(stats, planetStatus.players, planetStatus.retrieved_at)
    pos = planetInfo.position
    name = planet_base.name
    if "en-US" in planet_base.names:  # type: ignore
        name = planet_base.names.get("en-US", planet_base.name)
    planet = Planet(
        retrieved_at=planetStatus.retrieved_at,
        index=index,
        name=name,
        sector=planet_base.sector,
        biome=biome,
        hazards=env,
        hash=planetInfo.settingsHash,
        position=Position(x=pos.x, y=pos.y),
        waypoints=planetInfo.waypoints,
        maxHealth=planetInfo.maxHealth,
        health=planetStatus.health,
        disabled=planetInfo.disabled,
        initialOwner=faction_names.get(planetInfo.initialOwner, "???"),  # type: ignore
        currentOwner=faction_names.get(planetStatus.owner, "???"),  # type: ignore
        regenPerSecond=planetStatus.regenPerSecond,
        statistics=stats_new,
    )
    return planet


def check_compare_value(key, value, target: List[Dict[str, Any]]):
    for s in target:
        if s[key] == value:
            return s
    return None


def check_compare_value_list(keys: List[str], values: List[Any], target: List[Dict[str, Any]]):
    values = []
    for s in target:
        if all(s[key] == value for key, value in zip(keys, values)):
            values.append(s)
    return values


def get_time(status: WarStatus, info: WarInfo) -> dt.datetime:
    """get the relative start of the war according the game's internal "time" value"""

    # Get datetime diveharder object was retrieved at
    now = status.retrieved_at
    gametime = dt.datetime.fromtimestamp(info.startDate, tz=dt.timezone.utc) + dt.timedelta(
        seconds=status.time
    )
    deviation = now - gametime
    # print(deviation)
    relative_game_start = dt.datetime.fromtimestamp(info.startDate, tz=dt.timezone.utc) + deviation
    return relative_game_start


def get_time_dh(diveharder: DiveharderAll) -> dt.datetime:
    """get the relative start of the war according the game's internal "time" value using DiveharderAll"""

    status = diveharder.status
    info = diveharder.war_info
    return get_time(status, info)


def build_planet_full(
    planetIndex: int, status: WarStatus, info: WarInfo, summary: WarSummary, statics: StaticAll
) -> Planet:
    """
    Constructs a Planet object for a given planetIndex by associating the respective
    PlanetStatus, PlanetInfo, PlanetStats, PlanetEffects, PlanetAttacks, and
    PlanetEvents from the WarStatus, WarInfo, and WarSummary data obtained from the API,
    along with the static galaxy details.

    Args:
        planetIndex (int): The index of the planet to be constructed.
        status (WarStatus): Current state and status of the war.
        info (WarInfo): Information related to the ongoing war.
        summary (WarSummary): Summary statistics and data associated with the war.
        statics (StaticAll): Static game universe information.

    Returns:
        Planet: The constructed Planet object for the specified index.
    """

    # Get planet status & planet info
    planetStatus = check_compare_value("index", planetIndex, status.planetStatus)
    planetInfo = check_compare_value("index", planetIndex, info.planetInfos)
    if summary.planets_stats is not None:
        planetStatistics = check_compare_value("planetIndex", planetIndex, summary.planets_stats)
        if not planetStatistics:
            planetStatistics = PlanetStats(planetIndex=planetIndex)
    else:
        planetStatistics = PlanetStats(planetIndex=planetIndex)

    # Build Planet.
    planet = build_planet_basic(
        statics.galaxystatic, planetIndex, planetStatus, planetInfo, planetStatistics
    )
    planet.sector_id = planetInfo.sector  # type: ignore

    planet_effect_list = []
    planet_attack_list = []

    # Build Effects
    for effect in status.planetActiveEffects:
        if effect.index == planetIndex:
            effects = build_planet_effect(statics.effectstatic, effect.galacticEffectId)
            planet_effect_list.append(effects)

    planet.activePlanetEffects = planet_effect_list

    # Build Attacks
    for attack in status.planetAttacks:
        if attack.source == planetIndex:
            planet_attack_list.append(attack.target)

    planet.attacking = planet_attack_list

    # Build Events
    event: PlanetEvent = check_compare_value("planetIndex", planetIndex, status.planetEvents)  # type: ignore

    starttime = get_time(status, info)
    if event:
        newevent = Event(
            retrieved_at=event.retrieved_at,
            id=event.id,
            eventType=event.eventType,
            faction=faction_names.get(event.race, "???"),  # type: ignore
            health=event.health,
            maxHealth=event.maxHealth,
            startTime=(starttime + (dt.timedelta(seconds=event.startTime))).isoformat(),
            endTime=(starttime + (dt.timedelta(seconds=event.expireTime))).isoformat(),
            campaignId=event.campaignId,
            jointOperationIds=event.jointOperationIds,
        )
        planet.event = newevent
    return planet


def build_planet_2(planetIndex: int, warall: DiveharderAll, statics: StaticAll):
    """
    Constructs a Planet object for a given planetIndex by associating the respective
    PlanetStatus, PlanetInfo, PlanetStats, PlanetEffects, PlanetAttacks, and
    PlanetEvents from a DiveharderAll object and the static galaxy details.

    Args:
        planetIndex (int): The index of the planet to be constructed.
        warall (DiveharderAll): Operational game state and status data.
        statics (StaticAll): Static game universe information.

    Returns:
        Planet: The constructed Planet object for the specified index.
    """
    status: WarStatus = warall.status  # type: ignore
    info: WarInfo = warall.war_info  # type: ignore
    summary: Optional[WarSummary] = warall.planet_stats
    planet = build_planet_full(planetIndex, status, info, summary, statics)
    return planet


def build_all_planets(warall: DiveharderAll, statics: StaticAll) -> Dict[int, Planet]:
    """
    Builds a dictionary of all planets by iterating over the galaxy's static planet data
    and invoking build_planet_2 for each planet.

    Args:
        warall (DiveharderAll): Operational game state and status data.
        statics (StaticAll): Static information about the game's universe.

    Returns:
        dict: A dictionary mapping planet indices to Planet objects.
    """
    planet_data = {}
    for i, v in statics.galaxystatic.planets.items():
        status: WarStatus = warall.status  # type: ignore
        info: WarInfo = warall.war_info  # type: ignore
        summary: Optional[WarSummary] = warall.planet_stats
        planet = build_planet_full(i, status, info, summary, statics)
        planet_data[i] = planet
    return planet_data
