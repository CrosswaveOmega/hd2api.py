import pytest
import asyncio
from hd2api import *


@pytest.fixture
def apiconfig():
    return APIConfig()


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
