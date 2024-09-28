import pytest
import asyncio
from hd2api import *

import logging

hd2api_logger = logging.getLogger("hd2api_logger")


@pytest.fixture
def apiconfig():
    config = APIConfig()
    config.staticdata()

    return config


async def test_get_raw(apiconfig):
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiRawWarStatus(apiconfig)
    assert warstatus is not None
    print(warstatus.time)


async def test_get_direct(apiconfig):
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiDirectWarStatus(apiconfig)
    assert warstatus is not None
    print(warstatus.time)


async def test_get_direct_all(apiconfig):
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiRawAll(apiconfig)
    assert warstatus is not None
    timea = get_time(warstatus.status, warstatus.war_info)


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

    print(planeta)
