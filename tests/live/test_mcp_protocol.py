"""Integration tests that drive the tools through a real MCP client.

The rest of the live suite calls the typed tool functions directly and never
crosses the ``@mcp.tool()`` wrapper. These tests cover the layer direct calls
skip: registration via ``register_all``, the input schemas FastMCP derives from
type hints, output-schema serialization, and decoding real Mealie responses
through the wrapper.

The in-memory ``Client(mcp)`` crosses the full protocol boundary in-process for
the behavioural round-trips. One stdio subprocess smoke covers the real
``mcp.run()`` entrypoint and stdio framing.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import Callable

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from fastmcp.exceptions import ToolError

from mealie_mcp.server import mcp

ANCHOR_TOOLS = {
    "mealie_list_recipes",
    "mealie_create_recipe",
    "mealie_get_recipe",
    "mealie_delete_recipe",
}

ENVELOPE_KEYS = {"items", "page", "per_page", "total", "total_pages"}


@pytest.mark.live
def test_in_memory_client_enumerates_anchor_tools() -> None:
    async def run() -> set[str]:
        async with Client(mcp) as client:
            tools = await client.list_tools()
        return {tool.name for tool in tools}

    names = asyncio.run(run())
    assert names
    assert names >= ANCHOR_TOOLS


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_list_recipes_round_trips_pagination_envelope() -> None:
    async def run() -> object:
        async with Client(mcp) as client:
            result = await client.call_tool("mealie_list_recipes", {"per_page": 1})
        return result.data

    data = asyncio.run(run())
    assert isinstance(data, dict)
    assert set(data) >= ENVELOPE_KEYS
    assert isinstance(data["items"], list)


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_create_recipe_round_trips_name_through_wrapper(sentinel_name: str) -> None:
    async def run() -> str:
        async with Client(mcp) as client:
            created = await client.call_tool("mealie_create_recipe", {"name": sentinel_name})
            slug = created.data["slug"]
            try:
                fetched = await client.call_tool("mealie_get_recipe", {"slug_or_id": slug})
                return fetched.data["name"]
            finally:
                with contextlib.suppress(ToolError):
                    await client.call_tool("mealie_delete_recipe", {"slug_or_id": slug})

    fetched_name = asyncio.run(run())
    assert fetched_name == sentinel_name


# Groups whose create tool takes only a name and whose delete tool takes only
# the created id. One parametrized round-trip proves each forwards its argument
# through the wrapper; the richer groups carry their own round-trip in-file.
NAME_ONLY_GROUPS = [
    ("mealie_create_tag", "mealie_delete_tag", "item_id"),
    ("mealie_create_category", "mealie_delete_category", "item_id"),
    ("mealie_create_tool", "mealie_delete_tool", "item_id"),
    ("mealie_create_food", "mealie_delete_food", "item_id"),
    ("mealie_create_unit", "mealie_delete_unit", "item_id"),
    ("mealie_create_shopping_list", "mealie_delete_shopping_list", "list_id"),
]


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
@pytest.mark.parametrize(("create_tool", "delete_tool", "delete_key"), NAME_ONLY_GROUPS)
def test_name_only_create_round_trips_through_wrapper(
    create_tool: str,
    delete_tool: str,
    delete_key: str,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    created = call_tool(create_tool, {"name": sentinel_name})
    assert isinstance(created, dict)
    resource_id = created["id"]
    try:
        assert created["name"] == sentinel_name
    finally:
        with contextlib.suppress(ToolError):
            call_tool(delete_tool, {delete_key: resource_id})


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_stdio_entrypoint_boots_and_enumerates() -> None:
    async def run() -> set[str]:
        transport = StdioTransport(command="uv", args=["run", "mealie-mcp"])
        async with Client(transport) as client:
            tools = await client.list_tools()
        return {tool.name for tool in tools}

    names = asyncio.run(run())
    assert names
    assert names >= ANCHOR_TOOLS
