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
        "mealie_list_recipes",
        "mealie_duplicate_recipe",
        "mealie_update_last_made",
        "mealie_parse_recipe_url",
        "mealie_create_recipe_from_html_or_json",
        "mealie_create_comment",
        "mealie_get_comment",
        "mealie_list_comments",
        "mealie_list_recipe_comments",
        "mealie_update_comment",
        "mealie_delete_comment",
    }
