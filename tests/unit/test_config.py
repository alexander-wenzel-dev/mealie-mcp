"""Unit tests for the env-driven config loader."""

from __future__ import annotations

import pytest

from mealie_mcp.config import ConfigError, load_config


def test_load_config_returns_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MEALIE_BASE_URL", "https://mealie.example.com/")
    monkeypatch.setenv("MEALIE_API_TOKEN", "abc")
    config = load_config()
    assert config.base_url == "https://mealie.example.com"
    assert config.api_token == "abc"


def test_load_config_missing_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MEALIE_BASE_URL", raising=False)
    monkeypatch.setenv("MEALIE_API_TOKEN", "abc")
    with pytest.raises(ConfigError, match="MEALIE_BASE_URL"):
        load_config()


def test_load_config_missing_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MEALIE_BASE_URL", "https://mealie.example.com")
    monkeypatch.delenv("MEALIE_API_TOKEN", raising=False)
    with pytest.raises(ConfigError, match="MEALIE_API_TOKEN"):
        load_config()


def test_load_config_blank_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MEALIE_BASE_URL", "   ")
    monkeypatch.setenv("MEALIE_API_TOKEN", "")
    with pytest.raises(ConfigError) as excinfo:
        load_config()
    msg = str(excinfo.value)
    assert "MEALIE_BASE_URL" in msg
    assert "MEALIE_API_TOKEN" in msg
