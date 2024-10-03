from typing import List, Optional, Type, TypeVar

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *
from ..models.ABC.model import BaseApiModel
from .async_direct_service import GetApiDirectAll
from .service_utils import make_output

from .service_base import make_async_api_request

T = TypeVar("T", bound=BaseApiModel)
import random
import logging
from logging.handlers import RotatingFileHandler

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

    data = await make_async_api_request(base_path, path, api_config)

    return make_output(data, model, index)


async def make_comm_raw_api_request(
    endpoint: str,
    model: Type[T],
    index: Optional[int] = None,
    api_config_override: Optional[APIConfig] = None,
) -> Union[T, List[T]]:
    """
    Get a raw api object from the Community api.
    """
    api_config = api_config_override or APIConfig()

    base_path = api_config.api_comm
    path = f"/raw/api/{endpoint}"
    if index is not None:
        path += f"/{index}"

    data = await make_async_api_request(base_path, path, api_config)
    return make_output(data, model, index)


# Raw Community API Endpoints


async def GetCommApiRawWarStatus(api_config_override: Optional[APIConfig] = None) -> WarStatus:
    return await make_comm_raw_api_request(
        "WarSeason/801/Status", WarStatus, api_config_override=api_config_override
    )


async def GetCommApiRawWarInfo(api_config_override: Optional[APIConfig] = None) -> WarInfo:
    return await make_comm_raw_api_request(
        "WarSeason/801/WarInfo", WarInfo, api_config_override=api_config_override
    )


async def GetCommApiRawSummary(api_config_override: Optional[APIConfig] = None) -> WarSummary:
    return await make_comm_raw_api_request(
        "Stats/War/801/Summary", WarSummary, api_config_override=api_config_override
    )


async def GetCommApiRawAssignment(api_config_override: Optional[APIConfig] = None) -> Assignment:
    return await make_comm_raw_api_request(
        "v2/Assignment/War/801", Assignment, api_config_override=api_config_override
    )


async def GetCommApiRawNewsFeed(
    api_config_override: Optional[APIConfig] = None,
) -> List[NewsFeedItem]:
    return await make_comm_raw_api_request(
        "NewsFeed/801", NewsFeedItem, api_config_override=api_config_override
    )


# V1 Community API Endpoints


async def GetApiV1War(api_config_override: Optional[APIConfig] = None) -> War:
    return await make_comm_v1_api_request("war", War, api_config_override=api_config_override)


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


async def GetApiV1Planets(index: int, api_config_override: Optional[APIConfig] = None) -> Planet:
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
