"""Shared fixtures for live tests that hit a real Mealie instance.

Live tests are opt-in via the `live` marker. They require `MEALIE_BASE_URL` and
`MEALIE_API_TOKEN` to be set in the environment (typically through a `.env`
file the operator manages out of band).
"""

from __future__ import annotations

import asyncio
import datetime as dt
import os
from collections.abc import Callable, Iterator

import pytest
from fastmcp import Client

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client_factory import get_client, reset_client
from mealie_mcp.server import mcp


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


@pytest.fixture
def call_tool() -> Callable[[str, dict[str, object]], object]:
    """Drive a tool through its `@mcp.tool()` wrapper on an in-memory client.

    Returns the tool's `data` payload. A direct call to the typed function skips
    argument forwarding, the FastMCP-derived input schema, and output
    serialization; this crosses all three so a wrapper that forwards to the wrong
    parameter or mis-serializes its result is caught.
    """

    def _call(tool_name: str, arguments: dict[str, object]) -> object:
        async def run() -> object:
            async with Client(mcp) as client:
                result = await client.call_tool(tool_name, arguments)
            return result.data

        return asyncio.run(run())

    return _call
