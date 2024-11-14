#   ---------------------------------------------------------------------------------
#   Copyright (c) Microsoft Corporation. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""
This is a configuration file for pytest containing customizations and fixtures.

In VSCode, Code Coverage is recorded in config.xml. Delete this file to reset reporting.
"""

from __future__ import annotations

from logging.handlers import RotatingFileHandler
from typing import List

import pytest
from _pytest.nodes import Item
import logging

hd2api_logger = logging.getLogger("hd2api_logger")


def pytest_collection_modifyitems(items: list[Item]):
    for item in items:
        if "spark" in item.nodeid:
            item.add_marker(pytest.mark.spark)
        elif "_int_" in item.nodeid:
            item.add_marker(pytest.mark.integration)


@pytest.fixture
def unit_test_mocks(monkeypatch: None):
    """Include Mocks here to execute all commands offline and fast."""
    pass


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Set the formatter for the console handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S%p",
    )
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    hd2api_logger.addHandler(console_handler)
    log_handler = RotatingFileHandler(
        f"./logs/hd2api_logger.log", maxBytes=5 * 1024 * 1024, backupCount=5
    )

    log_handler.setLevel(logging.INFO)

    hd2api_logger.addHandler(log_handler)
