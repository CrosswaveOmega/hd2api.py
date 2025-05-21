import logging

hd2api_logger = logging.getLogger("hd2api_logger")

import math

import pytest

from hd2api import *
from hd2api.util.find import get_item


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
    print(allval.status.planetRegions)
    print(allval.war_info.planetRegions)
    regions = build_all_regions(allval, apiconfig.staticdata())
    assert regions
    for i in regions:
        print(i)


async def test_get_planet_name(apiconfig):
    allval = await GetApiRawAll(apiconfig)
    planets = build_all_planets(allval, apiconfig.staticdata())
    # print(planets)
    item = get_item(planets.values(), name="MERIDIA")
    # print(allval)
    assert item.name == "MERIDIA"
    return planets


async def test_station_get(apiconfig):
    apiconfig.use_raw = "direct"
    allval = await GetApiRawWarStatus(apiconfig)

    for i in allval.spaceStations:
        station = await GetApiRawSpaceStation(i.id32, apiconfig)
        hd2api_logger.info(str(station))
    # #print(allval)


async def test_positions(apiconfig):
    now = datetime.datetime.now()
    this = Position(x=0.1, y=0.2, retrieved_at=now)
    last = Position(x=0.1, y=0.1, retrieved_at=now - datetime.timedelta(minutes=5))

    last_speed = 0.05
    target = Position(x=0.0, y=0.0, retrieved_at=now)
    difference = this - last
    mag = difference.mag()
    # print("Mag is", mag)
    speed = difference.speed()
    # print("Speed is", speed * 60)
    current_angle = difference.angle()
    # print("Angle is", current_angle)
    if last_speed is not None:
        acceleration = (
            speed - last_speed
        ) / difference.time_delta.total_seconds()  # Acceleration in units/hr²
    else:
        acceleration = None  # First measurement, no acceleration
    # print("Acceleration is", acceleration)
    target_diff = target - this
    target_mag = target_diff.mag()
    target_angle = target_diff.angle()

    time_to_target = this.estimate_time_to_target(target, speed, acceleration)

    # print("Distance to target is", target_mag)
    # print(f"Current Trajectory: {current_angle:.2f}° (Clockwise from +Y-axis)")
    # print(f"Required Trajectory to Reach Target: {target_angle:.2f}° (Clockwise)")
    assert time_to_target != None
    # print(f"Time to Target: {time_to_target}\n")
