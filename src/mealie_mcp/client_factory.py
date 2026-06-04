"""Construct and own the authenticated Mealie API client.

Production code calls `get_client()` to share one process-scoped client whose
underlying httpx connection pool is opened on first use and closed at
interpreter shutdown. `build_client()` returns a fresh client for tests or
scripts that manage their own lifecycle.
"""

from __future__ import annotations

import atexit
import threading
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass

import httpx

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.config import load_config

DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=5.0)

ClientProvider = Callable[[], AuthenticatedClient]
"""A callable that returns the AuthenticatedClient to use for a tool call."""


@dataclass
class _Cache:
    client: AuthenticatedClient | None = None


_cache = _Cache()
_lock = threading.Lock()


def build_client() -> AuthenticatedClient:
    """Return a freshly constructed `AuthenticatedClient` with the project's
    default timeout. Callers own its lifecycle."""
    config = load_config()
    return AuthenticatedClient(
        base_url=config.base_url,
        token=config.api_token,
        timeout=DEFAULT_TIMEOUT,
    )


def get_client() -> AuthenticatedClient:
    """Return the process-scoped `AuthenticatedClient`, building it on first
    call. The underlying httpx client is opened so connections are pooled
    across tool invocations; `atexit` closes it at interpreter shutdown."""
    if _cache.client is not None:
        return _cache.client
    with _lock:
        if _cache.client is None:
            client = build_client()
            try:
                client.__enter__()
            except BaseException:
                with suppress(Exception):
                    client.__exit__(None, None, None)
                raise
            _cache.client = client
            atexit.register(_shutdown)
    return _cache.client


def reset_client() -> None:
    """Close any cached client and forget it.

    Intended for tests and process-shutdown code. Not safe to call while
    other threads or tasks may still be issuing requests; serialize at the
    caller if that situation can arise.
    """
    _shutdown()


def _shutdown() -> None:
    with _lock:
        client = _cache.client
        if client is None:
            return
        _cache.client = None
    with suppress(Exception):
        client.__exit__(None, None, None)
