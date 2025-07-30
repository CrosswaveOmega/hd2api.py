import logging
import datetime as dt
from collections import defaultdict, Counter


hd2api_logger = logging.getLogger("hd2api_logger")

import math

import pytest

from hd2api import *
from hd2api.util.find import get_item


@pytest.fixture
def apiconfig():
    config = APIConfig(client_contact="TEST_CONTACT")
    config.staticdata()

    return config


async def test_get_raw(apiconfig):
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiRawWarStatus(apiconfig)
    assert warstatus is not None
    # print(warstatus.time)


async def test_get_direct(apiconfig):
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiDirectWarStatus(apiconfig)
    assert warstatus is not None
    # print(warstatus.time)


async def test_get_direct_all(apiconfig):
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiRawAll(apiconfig)
    assert warstatus is not None
    timea = get_time(warstatus.status, warstatus.war_info)
    print(timea)


async def test_planet(apiconfig):
    allval = await GetApiRawAll(apiconfig)
    hd2api_logger.info(allval.status)
    planet = build_planet_2(64, allval, apiconfig.staticdata())
    hd2api_logger.info(planet)
    assert planet.name.upper() == "MERIDIA"


async def test_get_event_avg(apiconfig):
    """Test averaging for planet"""
    warall = await GetApiRawAll(apiconfig)

    assert warall is not None
    mockcampaign = Campaign(
        id=10,
        planetIndex=2,
        type=1,
        count=1,
    )
    mockevent = PlanetEvent(
        id=213,
        eventType=1,
        race=2,
        planetIndex=2,
        health=1000,
        maxHealth=1000,
        startTime=warall.status.time,
        expireTime=warall.status.time + 10000000,
        campaignId=10,
        jointOperationIds=[4],
    )
    warall.status.campaigns.append(mockcampaign)
    warall.status.planetEvents.append(mockevent)
    planeta = build_planet_2(2, warall, apiconfig.statics)
    hd2api_logger.info(str(planeta))
    mockevent.retrieved_at += datetime.timedelta(minutes=15)
    mockevent.health -= 100
    mockcampaign.retrieved_at += datetime.timedelta(minutes=15)
    planetb = build_planet_2(2, warall, apiconfig.statics)
    planetb.retrieved_at += datetime.timedelta(minutes=15)

    mockevent.retrieved_at += datetime.timedelta(minutes=15)
    mockevent.health -= 200
    mockcampaign.retrieved_at += datetime.timedelta(minutes=15)
    planetc = build_planet_2(2, warall, apiconfig.statics)
    planetc.retrieved_at += datetime.timedelta(minutes=30)
    hd2api_logger.info(str(planeta))
    hd2api_logger.info(str(planetb))
    hd2api_logger.info(str(planetc))
    diffs = [planetc - planetb, planetb - planeta]
    avg = Planet.average(diffs)

    hd2api_logger.info(str(avg))

    hd2api_logger.info(str(avg.event.health))
    assert avg.event.health == -150
    hd2api_logger.info(str(avg.time_delta))
    est = planetc.simple_planet_view(diffs[0], avg)
    hd2api_logger.info(str(est))

    # print(planeta)


async def test_get_regions(apiconfig):
    print("STAT")
    allval = await GetApiRawAll(apiconfig)
    # print(allval.status.planetRegions)
    # print(allval.war_info.planetRegions)
    regions = build_all_regions(allval, apiconfig.staticdata())
    assert regions
    for i in regions:
        # print(i)
        pass


async def test_get_planet_name(apiconfig):
    allval = await GetApiRawAll(apiconfig)
    planets = build_all_planets(allval, apiconfig.staticdata())
    # print(planets)
    item = get_item(planets.values(), name="MERIDIA")
    # print(allval)
    assert item.name == "MERIDIA"
    return planets


async def test_get_list_sector_names(apiconfig):
    allval = await GetApiRawAll(apiconfig, direct=True)
    planets = build_all_planets(allval, apiconfig.staticdata())

    sector_count = defaultdict(Counter)

    for plan in planets.values():
        sector_name = plan.sector
        sector_id = plan.sector_id
        sector_count[sector_name][sector_id] += 1

    result = [(name, dict(id_counts)) for name, id_counts in sector_count.items()]

    print(result)


async def test_station_get(apiconfig):
    apiconfig.use_raw = "direct"
    allval = await GetApiRawWarStatus(apiconfig)

    for i in allval.spaceStations:
        station = await GetApiRawSpaceStation(i.id32, apiconfig)
        hd2api_logger.info(str(station))
    # #print(allval)


async def test_languages(apiconfig):
    apiconfig.use_raw = "direct"
    languages = [
        "en-US",
        "en-GB",
        "pt-BR",
        "de-DE",
        "es-ES",
        "fr-FR",
        "it-IT",
        "ja-JP",
        "ko-KO",
        "ms-MY",
        "pl-PL",
        "pt-PT",
        "ru-RU",
        "zh-Hans",
        "zh-Hant",
    ]
    for l in languages:
        apiconfig.language = l
        allval = await GetApiDirectNewsFeed(apiconfig)
        if allval:
            print(l, "Is ok, size is", len(allval))

    # #print(allval)

    apiconfig.language = "en-US"


async def test_time_get(apiconfig):
    apiconfig.use_raw = "direct"
    warstatus = await GetApiRawAll(apiconfig)
    assert warstatus is not None
    timea = get_time(warstatus.status, warstatus.war_info)
    print(timea + dt.timedelta(seconds=warstatus.status.time))
    # #print(allval)
    print(timea + dt.timedelta(seconds=45795971))
    print(warstatus.status.time - 45795971)
    apiconfig.language = "en-US"
