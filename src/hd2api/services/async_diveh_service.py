from typing import List, Optional, Type, TypeVar

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *
from ..models.ABC.model import BaseApiModel
from .async_direct_service import GetApiDirectAll
from .service_utils import make_output

T = TypeVar("T", bound=BaseApiModel)

import logging

hd2api_logger = logging.getLogger("hd2api_logger")


async def make_raw_api_request(
    endpoint: str,
    model: Type[T],
    api_config_override: Optional[APIConfig] = None,
    path2=False,
    params: Optional[Dict] = None,  # Added parameters for GET requests
) -> Union[T, List[T]]:
    """
    Get a raw api object from diveharder.
    """
    api_config = api_config_override or APIConfig()

    base_path = api_config.api_diveharder
    path = f"/raw/{endpoint}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Super-Client": f"{api_config.get_client_name()}",
    }
    async with httpx.AsyncClient(
        base_url=base_path, verify=api_config.verify, timeout=api_config.timeout
    ) as client:
        response = await client.get(path, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f"Failed with status code: {response.status_code}"
        )

    data = response.json()
    return make_output(data, model, None)


async def GetDhApiRawWarStatus(api_config_override: Optional[APIConfig] = None) -> WarStatus:
    return await make_raw_api_request("status", WarStatus, api_config_override=api_config_override)


async def GetDhApiRawWarInfo(api_config_override: Optional[APIConfig] = None) -> WarInfo:
    return await make_raw_api_request("war_info", WarInfo, api_config_override=api_config_override)


async def GetDhApiRawSummary(api_config_override: Optional[APIConfig] = None) -> WarSummary:
    return await make_raw_api_request(
        "planet_stats", WarSummary, api_config_override=api_config_override
    )


async def GetDhApiRawAssignment(api_config_override: Optional[APIConfig] = None) -> Assignment:
    return await make_raw_api_request(
        "major_order", Assignment, api_config_override=api_config_override
    )


async def GetDhApiRawNewsFeed(
    api_config_override: Optional[APIConfig] = None,
) -> List[NewsFeedItem]:
    return await make_raw_api_request(
        "news_feed",
        NewsFeedItem,
        api_config_override=api_config_override,
        params={"maxEntries": 1024},
    )


async def GetDhApiRawAll(api_config_override: Optional[APIConfig] = None) -> DiveharderAll:
    return await make_raw_api_request(
        "all", DiveharderAll, api_config_override=api_config_override, path2=True
    )
