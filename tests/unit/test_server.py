"""Server-level wiring checks."""

from __future__ import annotations

import asyncio

from fastmcp import FastMCP

from mealie_mcp.server import mcp


def test_server_module_exposes_fastmcp_instance() -> None:
    assert isinstance(mcp, FastMCP)


def test_server_registers_expected_tools() -> None:
    tools = asyncio.run(mcp.list_tools())
    names = {tool.name for tool in tools}
    assert names == {
        "mealie_create_recipe",
        "mealie_get_recipe",
        "mealie_delete_recipe",
    }
