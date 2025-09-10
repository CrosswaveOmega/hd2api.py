import logging
from typing import List, Optional, Type, TypeVar, Union

from ..api_config import APIConfig, HTTPException
from ..models import (
    Assignment,
    DiveharderAll,
    NewsFeedItem,
    SpaceStation,
    WarInfo,
    WarStatus,
    WarSummary,
)
from ..models.ABC.model import BaseApiModel
from .service_base import make_async_api_request
from .service_utils import make_output

T = TypeVar("T", bound=BaseApiModel)


# Create a logger and set its level
hd2api_logger = logging.getLogger("hd2api_logger")
hd2api_logger.setLevel(logging.INFO)


async def make_direct_api_request(
    endpoint: str,
    model: Type[T],
    api_config_override: Optional[APIConfig] = None,
    params: Optional[dict] = None,  # Added parameters for GET requests
) -> Optional[Union[T, List[T]]]:
    """Get a raw api object directly from arrowhead's api."""
    api_config = api_config_override or APIConfig()

    base_path = api_config.api_direct
    path = f"/api/{endpoint}"

    data = await make_async_api_request(base_path, path, api_config, params)

    return make_output(data, model, None)


async def GetApiDirectWarStatus(
    api_config_override: Optional[APIConfig] = None,
) -> Optional[WarStatus]:
    result = await make_direct_api_request(
        "WarSeason/WARID/Status", WarStatus, api_config_override=api_config_override
    )

    # Check if result is a list or None, and raise an exception if needed
    if isinstance(result, list):
        raise TypeError("Expected a single WarStatus, but got a list.")
    elif result is None:
        raise ValueError("Failed to retrieve WarStatus.")

    return result  # Here, result is guaranteed to be a WarStatus


async def GetApiDirectWarInfo(
    api_config_override: Optional[APIConfig] = None,
) -> WarInfo:
    result = await make_direct_api_request(
        "WarSeason/WARID/WarInfo", WarInfo, api_config_override=api_config_override
    )

    if isinstance(result, list):
        raise TypeError("Expected a single WarInfo, but got a list.")
    elif result is None:
        raise ValueError("Failed to retrieve WarInfo.")

    return result  # Here, result is guaranteed to be WarInfo


async def GetApiDirectSummary(
    api_config_override: Optional[APIConfig] = None,
) -> WarSummary:
    result = await make_direct_api_request(
        "Stats/War/WARID/Summary", WarSummary, api_config_override=api_config_override
    )

    if isinstance(result, list):
        raise TypeError("Expected a single WarSummary, but got a list.")
    elif result is None:
        raise ValueError("Failed to retrieve WarSummary.")

    return result  # Here, result is guaranteed to be WarSummary


async def GetApiDirectAssignment(
    api_config_override: Optional[APIConfig] = None,
) -> List[Assignment]:
    result = await make_direct_api_request(
        "v2/Assignment/War/WARID", Assignment, api_config_override=api_config_override
    )

    if result is None:
        raise ValueError("Failed to retrieve Assignments.")

    if not isinstance(result, list):
        raise TypeError("Expected a list of Assignment, but got something else.")

    return result  # Here, result is guaranteed to be List[Assignment]


async def GetApiDirectNewsFeed(
    api_config_override: Optional[APIConfig] = None, fromTimestamp=None
) -> List[NewsFeedItem]:
    if fromTimestamp:
        result = await make_direct_api_request(
            "NewsFeed/WARID",
            NewsFeedItem,
            api_config_override=api_config_override,
            params={"maxEntries": 1024, "fromTimestamp": fromTimestamp},
        )
    else:
        result = await make_direct_api_request(
            "NewsFeed/WARID",
            NewsFeedItem,
            api_config_override=api_config_override,
            params={"maxEntries": 1024},
        )
    if result is None:
        raise ValueError("Failed to retrieve News Feed.")

    if not isinstance(result, list):
        raise TypeError("Expected a list of News Feed Items, but got something else.")

    return result


async def GetApiDirectSpaceStation(
    station_id: int,
    api_config_override: Optional[APIConfig] = None,
) -> SpaceStation:
    result = await make_direct_api_request(
        f"SpaceStation/WARID/{station_id}",
        SpaceStation,
        api_config_override=api_config_override,
    )
    if result is None:
        raise ValueError("Failed to retrieve Space Station.")

    return result


async def GetApiDirectAll(
    api_config_override: Optional[APIConfig] = None,
) -> DiveharderAll:
    warstatus = await GetApiDirectWarStatus(api_config_override)
    warinfo = await GetApiDirectWarInfo(api_config_override)
    summary = await GetApiDirectSummary(api_config_override)
    assign = await GetApiDirectAssignment(api_config_override)
    try:
        news = await GetApiDirectNewsFeed(
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
