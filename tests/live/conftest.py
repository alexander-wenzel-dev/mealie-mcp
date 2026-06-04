"""Shared fixtures for live tests that hit a real Mealie instance.

Live tests are opt-in via the `live` marker. They require `MEALIE_BASE_URL` and
`MEALIE_API_TOKEN` to be set in the environment (typically through a `.env`
file the operator manages out of band).
"""

from __future__ import annotations

import datetime as dt
import os
from collections.abc import Iterator

import pytest

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client_factory import get_client, reset_client


@pytest.fixture(scope="session")
def mealie_client() -> Iterator[AuthenticatedClient]:
    if not os.environ.get("MEALIE_BASE_URL") or not os.environ.get("MEALIE_API_TOKEN"):
        pytest.fail(
            "MEALIE_BASE_URL and MEALIE_API_TOKEN must be set for live tests. "
            "Copy .env.example to .env and fill in real values."
        )
    try:
        yield get_client()
    finally:
        reset_client()


@pytest.fixture
def sentinel_name() -> str:
    """Unique recipe name with the `mcp-test-` prefix and ISO timestamp."""
    stamp = dt.datetime.now(tz=dt.UTC).strftime("%Y%m%dT%H%M%S%f")
    return f"mcp-test-{stamp}"
