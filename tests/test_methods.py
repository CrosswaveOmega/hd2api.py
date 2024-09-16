#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is a sample python file for testing functions from the source code."""
from __future__ import annotations

import pytest
import asyncio
from helldive import *


async def test_get_raw():
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiRawWarStatus()
    assert warstatus is not None
    print(warstatus.time)


async def test_get_direct():
    """
    This defines the expected usage, which can then be used in various test cases.
    Pytest will not execute this code directly, since the function does not contain the suffex "test"
    """
    warstatus = await GetApiDirectWarStatus()
    assert warstatus is not None
    print(warstatus.time)
