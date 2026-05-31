"""Runtime configuration sourced from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


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
