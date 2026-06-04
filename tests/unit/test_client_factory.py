"""Tests for the authenticated-client factory.

These tests touch the singleton state in `mealie_mcp.client_factory`, so the
`_reset_client_cache` fixture resets it before and after each test.
"""

from __future__ import annotations

from collections.abc import Iterator

import httpx
import pytest

from mealie_mcp import client_factory
from mealie_mcp.client.client import AuthenticatedClient


@pytest.fixture(autouse=True)
def _reset_client_cache() -> Iterator[None]:
    client_factory.reset_client()
    yield
    client_factory.reset_client()


@pytest.fixture
def stub_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MEALIE_BASE_URL", "https://mealie.example.com")
    monkeypatch.setenv("MEALIE_API_TOKEN", "abc")


@pytest.mark.usefixtures("stub_env")
def test_build_client_uses_default_timeout() -> None:
    client = client_factory.build_client()
    assert isinstance(client, AuthenticatedClient)
    assert client.get_httpx_client().timeout == httpx.Timeout(30.0, connect=5.0)


@pytest.mark.usefixtures("stub_env")
def test_get_client_returns_same_instance() -> None:
    first = client_factory.get_client()
    second = client_factory.get_client()
    assert first is second


@pytest.mark.usefixtures("stub_env")
def test_reset_client_drops_cached_instance() -> None:
    first = client_factory.get_client()
    client_factory.reset_client()
    second = client_factory.get_client()
    assert first is not second
