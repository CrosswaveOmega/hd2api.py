import datetime as dt
from typing import Dict, List, Optional, Any

from ..constants import faction_names, region_size_enums
from ..models import (
    DiveharderAll,
    Event,
    GalaxyStatic,
    PlanetStatic,
    Planet,
    PlanetEvent,
    PlanetInfo,
    PlanetStats,
    PlanetStatus,
    Position,
    StaticAll,
    WarInfo,
    WarStatus,
    PlanetRegionInfo,
    PlanetRegion,
    PlanetRegionStatic,
    Region,
    WarSummary,
)
from ..util import get_item
from .effect_builder import build_planet_effect
from .statistics_builder import statistics_builder


def build_region(
    region: PlanetRegion, region_info: PlanetRegionInfo, statics: StaticAll
) -> Optional[Region]:
    """
    Builds a Region object from PlanetRegion, PlanetRegionInfo, and static data.

    Args:
        region (PlanetRegion): Dynamic state of the region.
        region_info (PlanetRegionInfo): Static info/config of the region.
        statics (StaticAll): Game-wide static data, used for name/description.

    Returns:
        Optional[Region]: A fully merged Region or None if static data not found.
    """
    if statics.galaxystatic is None or statics.galaxystatic.planetRegion is None:
        return None
    index = region_info.planetIndex if region_info.planetIndex is not None else -1
    planet_base = statics.galaxystatic.planets.get(
        index, PlanetStatic(name="UNKNOWN PLANET")
    )
    if not planet_base:
        return None
    if region_info.settingsHash in statics.galaxystatic.planetRegion:
        static_region = statics.galaxystatic.planetRegion[region_info.settingsHash]
    else:
        static_region = PlanetRegionStatic(name="UNNAMED", description="NoDescription")
    if not static_region:
        return None
    pname = planet_base.name
    if "en-US" in planet_base.names:  # type: ignore
        pname = planet_base.names.get("en-US", planet_base.name)

    keycombo = f"{region_info.planetIndex}_{region_info.regionIndex}"
    # Hash the keycombo into a 32-bit integer
    keycombo_hash = hash(keycombo) & 0xFFFFFFFF
    return Region(
        # From PlanetRegionInfo
        planetIndex=region_info.planetIndex,
        keyCombo=keycombo,
        id=keycombo_hash,
        planetName=pname,
        regionIndex=region_info.regionIndex,
        settingsHash=region_info.settingsHash,
        hash=region_info.settingsHash,
        maxHealth=region_info.maxHealth,
        regionSize=region_info.regionSize,
        size=region_size_enums.get(int(region_info.regionSize), region_info.regionSize),
        # From Static Region Metadata
        name=static_region.name,
        description=static_region.description,
        # From PlanetRegion (dynamic)
        owner=region.owner,
        health=region.health,
        regenPerSecond=region.regenPerSecond,
        availabilityFactor=region.availabilityFactor,
        isAvailable=region.isAvailable,
        players=region.players,
    )


def build_all_regions(warall: DiveharderAll, statics: StaticAll) -> List[Region]:
    """
    Merges all PlanetRegion and PlanetRegionInfo entries into Region objects.

    Returns:
        List[Region]: All fully merged region statuses.
    """
    result = []
    if (
        warall.status is None
        or warall.war_info is None
        or warall.status.planetRegions is None
        or warall.war_info.planetRegions is None
    ):
        print("NOTHING!")
        raise Exception(
            "Tried to build all regions when either status.planetRegions or war_info.planetRegions was empty!"
        )
        return result

    # Index PlanetRegionInfo by (planetIndex, regionIndex)
    status_lookup = {
        f"{info.planetIndex}_{info.regionIndex}": info
        for info in warall.status.planetRegions
    }

    for region in warall.war_info.planetRegions:
        key = f"{region.planetIndex}_{region.regionIndex}"
        region_info = status_lookup.get(key)
        if region_info:
            status = build_region(region_info, region, statics)
            if status:
                result.append(status)
        else:
            region_info = PlanetRegion(
                planetIndex=region.planetIndex,
                regionIndex=region.regionIndex,
                regenPerSecond=0.0,
                owner=None,
                health=region.maxHealth,
                availabilityFactor=0.0,
                isAvailable=False,
                players=0,
            )
            status = build_region(region_info, region, statics)
            if status:
                result.append(status)

    return result
