import logging
from typing import Any, Optional, TypeVar

import httpx

from ..api_config import APIConfig, HTTPException
from ..models.ABC.model import BaseApiModel

T = TypeVar("T", bound=BaseApiModel)


# Create a logger and set its level
hd2api_logger = logging.getLogger("hd2api_logger")
hd2api_logger.setLevel(logging.INFO)


async def make_async_api_request(
    base_path: str, path: str, api_config: APIConfig, params: Optional[dict] = None
) -> Any:
    """Make a asyncronous request to any endpoint."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Super-Client": f"{api_config.get_client_name()}",
        "Accept-Language": api_config.language,
    }
    if api_config.client_contact:
        headers["X-Super-Contact"] = api_config.client_contact
    # Replace WARID in path.
    if "WARID" in path:
        path = path.replace("WARID", f"{api_config.warID}")
    try:
        async with httpx.AsyncClient(
            base_url=base_path, verify=api_config.verify, timeout=api_config.timeout
        ) as client:
            if params:
                response = await client.get(
                    path, headers=headers, params=params
                )  # Added params to the request
            else:
                response = await client.get(
                    path, headers=headers
                )  # Added params to the request
    except httpx.HTTPError as e:
        print(e)
        hd2api_logger.error(str(e), exc_info=e)
        raise e

    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f"Failed with status code: {response.status_code}"
        )

    data = response.json()
    return data


def make_sync_api_request(
    base_path: str, path: str, api_config: APIConfig, params: Optional[dict] = None
) -> Any:
    """Make a synchronous request to any endpoint."""

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Super-Client": f"{api_config.get_client_name()}",
        "Accept-Language": api_config.language,
    }

    try:
        with httpx.Client(
            base_url=base_path, verify=api_config.verify, timeout=api_config.timeout
        ) as client:
            if params:
                response = client.get(path, headers=headers, params=params)
            else:
                response = client.get(path, headers=headers)
    except httpx.HTTPError as e:
        print(e)
        hd2api_logger.error(str(e), exc_info=e)
        raise e

    if response.status_code != 200:
        raise HTTPException(
            response.status_code, f"Failed with status code: {response.status_code}"
        )

    data = response.json()
    return data
