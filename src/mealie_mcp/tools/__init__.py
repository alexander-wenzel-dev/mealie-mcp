"""MCP tool implementations, grouped by Mealie OpenAPI tag.

Each submodule mirrors a folder under `mealie_mcp.client.api` and exposes a
`register(mcp)` function that the server uses to wire its tools.
"""

from __future__ import annotations

from fastmcp import FastMCP

from mealie_mcp.tools import organizer_categories, organizer_tags, recipe_comments, recipe_crud


def register_all(mcp: FastMCP) -> None:
    """Register every tool module with the given FastMCP instance."""
    recipe_crud.register(mcp)
    recipe_comments.register(mcp)
    organizer_categories.register(mcp)
    organizer_tags.register(mcp)
