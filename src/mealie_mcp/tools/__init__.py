"""MCP tool implementations, grouped by Mealie OpenAPI tag.

Each submodule mirrors a folder under `mealie_mcp.client.api` and exposes a
`register(mcp, get_client)` function that the server uses to wire its tools.
Submodules are discovered automatically, so adding a new group is a single-
file change.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterator
from types import ModuleType

from fastmcp import FastMCP

from mealie_mcp.client_factory import ClientProvider


def _iter_tool_modules() -> Iterator[ModuleType]:
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        if hasattr(module, "register"):
            yield module


def register_all(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register every tool module with the given FastMCP instance."""
    for module in _iter_tool_modules():
        module.register(mcp, get_client)
