from typing import List, TypeVar


from ..api_config import APIConfig
from ..models import *
from ..models.ABC.model import BaseApiModel
from .async_direct_service import (
    GetApiDirectAssignment,
    GetApiDirectWarStatus,
    GetApiDirectSummary,
    GetApiDirectWarInfo,
    GetApiDirectNewsFeed,
    GetApiDirectAll,
)
from .async_comm_service import (
    GetCommApiRawWarStatus,
    GetCommApiRawWarInfo,
    GetCommApiRawSummary,
    GetCommApiRawAssignment,
    GetCommApiRawNewsFeed,
)
from .async_diveh_service import (
    GetDhApiRawAssignment,
    GetDhApiRawWarInfo,
    GetDhApiRawWarStatus,
    GetDhApiRawNewsFeed,
    GetDhApiRawSummary,
    GetDhApiRawAll,
)

T = TypeVar("T", bound=BaseApiModel)
import logging

hd2api_logger = logging.getLogger("hd2api_logger")


async def GetApiRawWarStatus(api_config_override: APIConfig) -> WarStatus:
    """Retrieve the raw war status from the default raw api."""
    if api_config_override.use_raw == "community":
        return await GetCommApiRawWarStatus(api_config_override)
    elif api_config_override.use_raw == "diveharder":
        return await GetDhApiRawWarStatus(api_config_override)
    elif api_config_override.use_raw == "direct":
        return await GetApiDirectWarStatus(api_config_override)


async def GetApiRawWarInfo(api_config_override: APIConfig) -> WarInfo:
    """Retrieve the additional war info from the default raw api."""
    if api_config_override.use_raw == "community":
        return await GetCommApiRawWarInfo(api_config_override)
    elif api_config_override.use_raw == "diveharder":
        return await GetDhApiRawWarInfo(api_config_override)
    elif api_config_override.use_raw == "direct":
        return await GetApiDirectWarInfo(api_config_override)


async def GetApiRawSummary(api_config_override: APIConfig) -> WarSummary:
    """Retrieve the raw war summary from the default raw api."""
    if api_config_override.use_raw == "community":
        return await GetCommApiRawSummary(api_config_override)
    elif api_config_override.use_raw == "diveharder":
        return await GetDhApiRawSummary(api_config_override)
    elif api_config_override.use_raw == "direct":
        return await GetApiDirectSummary(api_config_override)


async def GetApiRawAssignment(api_config_override: APIConfig) -> Assignment:
    """Retrieve the raw assignment from the default raw api."""
    if api_config_override.use_raw == "community":
        return await GetCommApiRawAssignment(api_config_override)
    elif api_config_override.use_raw == "diveharder":
        return await GetDhApiRawAssignment(api_config_override)
    elif api_config_override.use_raw == "direct":
        return await GetApiDirectAssignment(api_config_override)


async def GetApiRawNewsFeed(api_config_override: APIConfig) -> List[NewsFeedItem]:
    """Retrieve the raw news feed from the default raw api."""
    if api_config_override.use_raw == "community":
        return await GetCommApiRawNewsFeed(api_config_override)
    elif api_config_override.use_raw == "diveharder":
        return await GetDhApiRawNewsFeed(api_config_override)
    elif api_config_override.use_raw == "direct":
        return await GetApiDirectNewsFeed(api_config_override)


async def GetApiRawAll(api_config_override: APIConfig, direct=False) -> DiveharderAll:
    """Retrieve all raw data from the api, optionally using the direct method."""
    if direct:
        return await GetApiDirectAll(api_config_override)
    else:
        return await GetDhApiRawAll(api_config_override)
