"""MCP tool implementations, grouped by Mealie OpenAPI tag.

Each submodule mirrors a folder under `mealie_mcp.client.api` and exposes a
`register(mcp, get_client)` function that the server uses to wire its tools.
Submodules are discovered automatically, so adding a new group is a single-
file change.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable, Iterator
from types import ModuleType
from typing import cast

from fastmcp import FastMCP

from mealie_mcp.client_factory import ClientProvider

Register = Callable[[FastMCP, ClientProvider], None]


def _require_register(module: ModuleType) -> Register:
    """Return a tool module's `register` callable, raising if it has none.

    A non-underscore module under this package is a tool group and must expose
    `register(mcp, get_client)`. Skipping one that does not would hide every
    tool it defines behind a green merge gate.
    """
    register = getattr(module, "register", None)
    if not callable(register):
        raise TypeError(
            f"tool module {module.__name__!r} defines no register callable; "
            "every non-underscore module under this package must expose "
            "register(mcp, get_client)"
        )
    return cast(Register, register)


def _iter_group_registers() -> Iterator[Register]:
    """Yield each tool group's register callable, one per non-underscore module."""
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        yield _require_register(module)


def register_all(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register every tool module with the given FastMCP instance."""
    for register in _iter_group_registers():
        register(mcp, get_client)
