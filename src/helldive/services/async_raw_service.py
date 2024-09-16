from typing import List, Optional, Type, TypeVar

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *
from ..models.ABC.model import BaseApiModel
from .async_direct_service import GetApiDirectAll
from .utils import make_output

T = TypeVar("T", bound=BaseApiModel)

import logging

logslogger = logging.getLogger("logslogger")


async def make_raw_api_request(
    endpoint: str,
    model: Type[T],
    index: Optional[int] = None,
    api_config_override: Optional[APIConfig] = None,
    path2=False,
) -> Union[T, List[T]]:
    """
    Get a raw api object from the Community api or
    diveharder.
    """
    api_config = api_config_override or APIConfig()

    base_path = api_config.api_comm
    path = f"/raw/api/{endpoint}"
    if index is not None:
        path += f"/{index}"

    if path2:
        base_path = api_config.api_diveharder
        path = f"/raw/{endpoint}"
        if index is not None:
            path += f"/{index}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Super-Client": f"{api_config.get_client_name()}",
        # "Authorization": f"Bearer {api_config.get_access_token()}",
    }
    async with httpx.AsyncClient(base_url=base_path, verify=api_config.verify, timeout=8.0) as client:
        response = await client.get(path, headers=headers)

    if response.status_code != 200:
        raise HTTPException(response.status_code, f"Failed with status code: {response.status_code}")
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    data = response.json()
    return make_output(data, model, index)


async def GetApiRawWarStatus(api_config_override: Optional[APIConfig] = None) -> WarStatus:
    return await make_raw_api_request("WarSeason/801/Status", WarStatus, api_config_override=api_config_override)


async def GetApiRawWarInfo(api_config_override: Optional[APIConfig] = None) -> WarInfo:
    return await make_raw_api_request("WarSeason/801/WarInfo", WarInfo, api_config_override=api_config_override)


async def GetApiRawSummary(api_config_override: Optional[APIConfig] = None) -> WarSummary:
    return await make_raw_api_request("Stats/War/801/Summary", WarSummary, api_config_override=api_config_override)


async def GetApiRawAssignment(api_config_override: Optional[APIConfig] = None) -> Assignment:
    return await make_raw_api_request("v2/Assignment/War/801", Assignment, api_config_override=api_config_override)


async def GetApiRawNewsFeed(api_config_override: Optional[APIConfig] = None) -> List[NewsFeedItem]:
    return await make_raw_api_request(
        "NewsFeed/801",
        NewsFeedItem,
        api_config_override=api_config_override,
        params={"maxEntries": 1024},
    )


async def GetApiRawAll(api_config_override: Optional[APIConfig] = None, direct=False) -> DiveharderAll:
    if direct:
        return await GetApiDirectAll(api_config_override=api_config_override)
    try:
        return await make_raw_api_request("all", DiveharderAll, api_config_override=api_config_override, path2=True)
    except Exception as e:
        logslogger.error(str(e), exc_info=e)
        return await GetApiDirectAll(api_config_override=api_config_override)
