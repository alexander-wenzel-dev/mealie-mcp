"""Runtime configuration sourced from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

MAX_PORT = 65535


class ConfigError(RuntimeError):
    """Raised when required configuration is missing."""


@dataclass(frozen=True, slots=True)
class Config:
    base_url: str
    api_token: str


def load_config() -> Config:
    """Read MEALIE_BASE_URL and MEALIE_API_TOKEN from the environment.

    Raises ConfigError if either is missing or empty.
    """
    base_url = os.environ.get("MEALIE_BASE_URL", "").strip()
    api_token = os.environ.get("MEALIE_API_TOKEN", "").strip()
    missing = [
        name
        for name, value in (
            ("MEALIE_BASE_URL", base_url),
            ("MEALIE_API_TOKEN", api_token),
        )
        if not value
    ]
    if missing:
        raise ConfigError("Missing required environment variable(s): " + ", ".join(missing))
    return Config(base_url=base_url.rstrip("/"), api_token=api_token)


@dataclass(frozen=True, slots=True)
class TransportConfig:
    transport: str
    host: str
    port: int
    allowed_hosts: tuple[str, ...]
    auth_token: str = ""


def load_transport_config() -> TransportConfig:
    """Read the transport settings that select stdio or HTTP serving.

    Defaults to stdio, where the host, port, token, and allowed-hosts values are
    unused. When MEALIE_MCP_TRANSPORT is http, a bearer token is mandatory: the
    server holds an admin Mealie token, so it refuses to serve HTTP without one.
    Raises ConfigError on an unknown transport, an unparsable port, or a missing
    HTTP token.
    """
    transport = os.environ.get("MEALIE_MCP_TRANSPORT", "stdio").strip().lower() or "stdio"
    if transport not in ("stdio", "http"):
        raise ConfigError(f"MEALIE_MCP_TRANSPORT must be 'stdio' or 'http', got {transport!r}")
    if transport == "stdio":
        return TransportConfig(
            transport="stdio",
            host="127.0.0.1",
            port=8000,
            allowed_hosts=(),
        )

    auth_token = os.environ.get("MEALIE_MCP_HTTP_TOKEN", "").strip()
    if not auth_token:
        raise ConfigError(
            "HTTP transport requires MEALIE_MCP_HTTP_TOKEN; generate one with scripts/gen-token"
        )
    host = os.environ.get("MEALIE_MCP_HTTP_HOST", "127.0.0.1").strip() or "127.0.0.1"
    port_raw = os.environ.get("MEALIE_MCP_HTTP_PORT", "8000").strip() or "8000"
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise ConfigError(f"MEALIE_MCP_HTTP_PORT must be an integer, got {port_raw!r}") from exc
    if not 1 <= port <= MAX_PORT:
        raise ConfigError(f"MEALIE_MCP_HTTP_PORT must be between 1 and {MAX_PORT}, got {port}")
    allowed_raw = (
        os.environ.get("MEALIE_MCP_HTTP_ALLOWED_HOSTS", "").strip() or "127.0.0.1,localhost"
    )
    allowed_hosts = tuple(entry for entry in (h.strip() for h in allowed_raw.split(",")) if entry)
    return TransportConfig(
        transport="http",
        host=host,
        port=port,
        auth_token=auth_token,
        allowed_hosts=allowed_hosts,
    )
