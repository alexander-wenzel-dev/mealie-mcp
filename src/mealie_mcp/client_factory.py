"""Construct the authenticated Mealie API client from runtime configuration."""

from __future__ import annotations

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.config import load_config


def build_client() -> AuthenticatedClient:
    """Return a fresh `AuthenticatedClient` for the configured Mealie instance."""
    config = load_config()
    return AuthenticatedClient(base_url=config.base_url, token=config.api_token)
