"""Server-level wiring checks."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from typing import cast

import pytest
from fastmcp import FastMCP
from starlette.requests import Request

from mealie_mcp.server import build_auth, health, mcp
from mealie_mcp.tools import _require_register


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


def test_require_register_returns_the_callable() -> None:
    def register(mcp: object, get_client: object) -> None: ...

    module = SimpleNamespace(__name__="mealie_mcp.tools.fake", register=register)
    assert _require_register(module) is register


def test_require_register_rejects_a_module_without_register() -> None:
    module = SimpleNamespace(__name__="mealie_mcp.tools.fake")
    with pytest.raises(TypeError, match="no register callable"):
        _require_register(module)


def test_require_register_rejects_a_non_callable_register() -> None:
    module = SimpleNamespace(__name__="mealie_mcp.tools.fake", register="not callable")
    with pytest.raises(TypeError, match="no register callable"):
        _require_register(module)


def test_health_route_reports_ok() -> None:
    response = asyncio.run(health(cast(Request, SimpleNamespace())))
    assert response.status_code == 200
    assert json.loads(response.body) == {"status": "ok"}


def test_build_auth_accepts_the_configured_token() -> None:
    verifier = build_auth("secret")
    assert "secret" in verifier.tokens
