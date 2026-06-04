"""Server-level wiring checks."""

from __future__ import annotations

import asyncio

from fastmcp import FastMCP

from mealie_mcp.server import mcp


def test_server_module_exposes_fastmcp_instance() -> None:
    assert isinstance(mcp, FastMCP)


def test_server_registers_unique_prefixed_tools() -> None:
    """All registered tools use the `mealie_` prefix and have unique names.

    Tool modules are auto-discovered, so an exact-set check would just
    re-type the names. Structural assertions keep this test stable as new
    groups are added.
    """
    tools = asyncio.run(mcp.list_tools())
    names = [tool.name for tool in tools]
    assert names, "expected at least one registered tool"
    assert len(names) == len(set(names)), f"duplicate tool names: {names}"
    bad = [n for n in names if not n.startswith("mealie_")]
    assert not bad, f"tool names must use the 'mealie_' prefix: {bad}"
