import logging
from typing import List, Optional, Type, TypeVar, Union

from hd2api.models import DiveharderAll

from ..api_config import APIConfig, HTTPException
from ..models import (
    Assignment,
    Assignment2,
    Campaign2,
    Dispatch,
    NewsFeedItem,
    Planet,
    SpaceStation,
    SteamNews,
    War,
    WarInfo,
    WarStatus,
    WarSummary,
)
from ..models.ABC.model import BaseApiModel
from .service_base import make_async_api_request
from .service_utils import make_output

T = TypeVar("T", bound=BaseApiModel)

hd2api_logger = logging.getLogger("hd2api_logger")


async def make_comm_v1_api_request(
    endpoint: str,
    model: Type[T],
    index: Optional[int] = None,
    api_config_override: Optional[APIConfig] = None,
) -> Union[T, List[T]]:
    """Make an API Request for a built object using the Community API Wrapper."""
    api_config = api_config_override or APIConfig()

    base_path = api_config.api_comm
    path = f"/api/v1/{endpoint}"
    if index is not None:
        path += f"/{index}"

    if api_config.client_contact is None:
        raise ValueError(
            "Attempted to call community api without setting client_contact"
        )

    data = await make_async_api_request(base_path, path, api_config)

    return make_output(data, model, index)


async def make_comm_raw_api_request(
    endpoint: str,
    model: Type[T],
    index: Optional[int] = None,
    api_config_override: Optional[APIConfig] = None,
    params: Optional[dict] = None,  # Added parameters for GET requests
) -> Union[T, List[T]]:
    """
    Get a raw api object from the Community api.
    """
    api_config = api_config_override or APIConfig()

    base_path = api_config.api_comm
    path = f"/raw/api/{endpoint}"
    if index is not None:
        path += f"/{index}"

    if api_config.client_contact is None:
        raise ValueError(
            "Attempted to call community api without setting client_contact"
        )

    data = await make_async_api_request(base_path, path, api_config, params)
    return make_output(data, model, index)


# Raw Community API Endpoints


async def GetCommApiRawWarStatus(
    api_config_override: Optional[APIConfig] = None,
) -> WarStatus:
    return await make_comm_raw_api_request(
        "WarSeason/WARID/Status", WarStatus, api_config_override=api_config_override
    )


async def GetCommApiRawWarInfo(
    api_config_override: Optional[APIConfig] = None,
) -> WarInfo:
    return await make_comm_raw_api_request(
        "WarSeason/WARID/WarInfo", WarInfo, api_config_override=api_config_override
    )


async def GetCommApiRawSummary(
    api_config_override: Optional[APIConfig] = None,
) -> WarSummary:
    return await make_comm_raw_api_request(
        "Stats/War/WARID/Summary", WarSummary, api_config_override=api_config_override
    )


async def GetCommApiRawAssignment(
    api_config_override: Optional[APIConfig] = None,
) -> Assignment:
    return await make_comm_raw_api_request(
        "v2/Assignment/War/WARID", Assignment, api_config_override=api_config_override
    )


async def GetCommApiRawNewsFeed(
    api_config_override: Optional[APIConfig] = None, fromTimestamp=None
) -> List[NewsFeedItem]:
    if fromTimestamp:
        return await make_comm_raw_api_request(
            "NewsFeed/WARID",
            NewsFeedItem,
            api_config_override=api_config_override,
            params={"maxEntries": 1024, "fromTimestamp": fromTimestamp},
        )
    return await make_comm_raw_api_request(
        "NewsFeed/WARID", NewsFeedItem, api_config_override=api_config_override
    )


async def GetCommApiRawSpaceStation(
    station_id: int,
    api_config_override: Optional[APIConfig] = None,
) -> SpaceStation:
    result = await make_comm_raw_api_request(
        f"SpaceStation/WARID/{station_id}",
        SpaceStation,
        api_config_override=api_config_override,
    )
    if result is None:
        raise ValueError("Failed to retrieve Space Station.")

    return result


# V1 Community API Endpoints


async def GetApiV1War(api_config_override: Optional[APIConfig] = None) -> War:
    return await make_comm_v1_api_request(
        "war", War, api_config_override=api_config_override
    )


async def GetApiV1AssignmentsAll(
    api_config_override: Optional[APIConfig] = None,
) -> List[Assignment2]:
    return await make_comm_v1_api_request(
        "assignments", Assignment2, api_config_override=api_config_override
    )


async def GetApiV1Assignments(
    index: int, api_config_override: Optional[APIConfig] = None
) -> Assignment2:
    return await make_comm_v1_api_request(
        "assignments", Assignment2, index, api_config_override=api_config_override
    )


async def GetApiV1CampaignsAll(
    api_config_override: Optional[APIConfig] = None,
) -> List[Campaign2]:
    return await make_comm_v1_api_request(
        "campaigns", Campaign2, api_config_override=api_config_override
    )


async def GetApiV1Campaigns(
    index: int, api_config_override: Optional[APIConfig] = None
) -> Campaign2:
    return await make_comm_v1_api_request(
        "campaigns", Campaign2, index, api_config_override=api_config_override
    )


async def GetApiV1DispatchesAll(
    api_config_override: Optional[APIConfig] = None,
) -> List[Dispatch]:
    return await make_comm_v1_api_request(
        "dispatches", Dispatch, api_config_override=api_config_override
    )


async def GetApiV1Dispatches(
    index: int, api_config_override: Optional[APIConfig] = None
) -> Dispatch:
    return await make_comm_v1_api_request(
        "dispatches", Dispatch, index, api_config_override=api_config_override
    )


async def GetApiV1PlanetsAll(
    api_config_override: Optional[APIConfig] = None,
) -> List[Planet]:
    return await make_comm_v1_api_request(
        "planets", Planet, api_config_override=api_config_override
    )


async def GetApiV1Planets(
    index: int, api_config_override: Optional[APIConfig] = None
) -> Planet:
    return await make_comm_v1_api_request(
        "planets", Planet, index, api_config_override=api_config_override
    )


async def GetApiV1PlanetEvents(
    api_config_override: Optional[APIConfig] = None,
) -> List[Planet]:
    return await make_comm_v1_api_request(
        "planet-events", Planet, api_config_override=api_config_override
    )


async def GetApiV1Steam(
    api_config_override: Optional[APIConfig] = None,
) -> List[SteamNews]:
    return await make_comm_v1_api_request(
        "steam", SteamNews, api_config_override=api_config_override
    )


async def GetApiV1Steam2(
    gid: str, api_config_override: Optional[APIConfig] = None
) -> List[SteamNews]:
    return await make_comm_v1_api_request(
        "steam", SteamNews, gid, api_config_override=api_config_override
    )


# Get all


async def GetCommApiRawAll(
    api_config_override: Optional[APIConfig] = None,
) -> DiveharderAll:
    warstatus = await GetCommApiRawWarStatus(api_config_override)
    warinfo = await GetCommApiRawWarInfo(api_config_override)
    summary = await GetCommApiRawSummary(api_config_override)
    assign = await GetCommApiRawAssignment(api_config_override)
    try:
        news = await GetCommApiRawNewsFeed(
            api_config_override, fromTimestamp=warstatus.time - 10000000
        )
    except HTTPException as e:
        hd2api_logger.error("Error raised when calling news feed: %s", e)
        news = None
    newdive = DiveharderAll(
        status=warstatus,
        war_info=warinfo,
        planet_stats=summary,
        major_order=assign,
        news_feed=news,
    )
    return newdive
