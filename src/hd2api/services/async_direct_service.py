from typing import List, Optional, Type, TypeVar

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *
from ..models.ABC.model import BaseApiModel
from .service_utils import make_output

from .service_base import make_async_api_request

T = TypeVar("T", bound=BaseApiModel)

import logging

# Create a logger and set its level
hd2api_logger = logging.getLogger("hd2api_logger")
hd2api_logger.setLevel(logging.INFO)


async def make_direct_api_request(
    endpoint: str,
    model: Type[T],
    index: Optional[int] = None,
    api_config_override: Optional[APIConfig] = None,
    path2=False,
    params: Optional[dict] = None,  # Added parameters for GET requests
) -> Optional[Union[T, List[T]]]:
    """Get a raw api object directly from arrowhead's api."""
    api_config = api_config_override or APIConfig()

    base_path = api_config.api_direct
    path = f"/api/{endpoint}"
    if index is not None:
        path += f"/{index}"
    data = await make_async_api_request(base_path, path, api_config, params)

    return make_output(data, model, index)


async def GetApiDirectWarStatus(
    api_config_override: Optional[APIConfig] = None,
) -> Optional[WarStatus]:
    result = await make_direct_api_request(
        "WarSeason/801/Status", WarStatus, api_config_override=api_config_override
    )

    # Check if result is a list or None, and raise an exception if needed
    if isinstance(result, list):
        raise TypeError("Expected a single WarStatus, but got a list.")
    elif result is None:
        raise ValueError("Failed to retrieve WarStatus.")

    return result  # Here, result is guaranteed to be a WarStatus


async def GetApiDirectWarInfo(api_config_override: Optional[APIConfig] = None) -> WarInfo:
    result = await make_direct_api_request(
        "WarSeason/801/WarInfo", WarInfo, api_config_override=api_config_override
    )

    if isinstance(result, list):
        raise TypeError("Expected a single WarInfo, but got a list.")
    elif result is None:
        raise ValueError("Failed to retrieve WarInfo.")

    return result  # Here, result is guaranteed to be WarInfo


async def GetApiDirectSummary(api_config_override: Optional[APIConfig] = None) -> WarSummary:
    result = await make_direct_api_request(
        "Stats/War/801/Summary", WarSummary, api_config_override=api_config_override
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
        "v2/Assignment/War/801", Assignment, api_config_override=api_config_override
    )

    if result is None:
        raise ValueError("Failed to retrieve Assignments.")

    if not isinstance(result, list):
        raise TypeError("Expected a list of Assignment, but got something else.")

    return result  # Here, result is guaranteed to be List[Assignment]


async def GetApiDirectNewsFeed(
    api_config_override: Optional[APIConfig] = None,
) -> List[NewsFeedItem]:
    result = await make_direct_api_request(
        "NewsFeed/801",
        NewsFeedItem,
        api_config_override=api_config_override,
        params={"maxEntries": 1024},
    )
    if result is None:
        raise ValueError("Failed to retrieve News Feed.")

    if not isinstance(result, list):
        raise TypeError("Expected a list of News Feed Items, but got something else.")

    return result


async def GetApiDirectAll(api_config_override: Optional[APIConfig] = None) -> DiveharderAll:
    warstatus = await GetApiDirectWarStatus(api_config_override)
    warinfo = await GetApiDirectWarInfo(api_config_override)
    summary = await GetApiDirectSummary(api_config_override)
    assign = await GetApiDirectAssignment(api_config_override)
    news = await GetApiDirectNewsFeed(api_config_override)

    newdive = DiveharderAll(
        status=warstatus,
        war_info=warinfo,
        planet_stats=summary,
        major_order=assign,
        news_feed=news,
    )
    return newdive
