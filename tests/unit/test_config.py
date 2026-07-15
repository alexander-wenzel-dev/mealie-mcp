"""Unit tests for the env-driven config loader."""

from __future__ import annotations

import pytest

from mealie_mcp.config import ConfigError, load_config, load_transport_config


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


def _clear_transport_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "MEALIE_MCP_TRANSPORT",
        "MEALIE_MCP_HTTP_TOKEN",
        "MEALIE_MCP_HTTP_HOST",
        "MEALIE_MCP_HTTP_PORT",
        "MEALIE_MCP_HTTP_ALLOWED_HOSTS",
    ):
        monkeypatch.delenv(name, raising=False)


def test_transport_defaults_to_stdio(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_transport_env(monkeypatch)
    config = load_transport_config()
    assert config.transport == "stdio"
    assert config.auth_token == ""


def test_transport_rejects_unknown_value(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_transport_env(monkeypatch)
    monkeypatch.setenv("MEALIE_MCP_TRANSPORT", "sse")
    with pytest.raises(ConfigError, match="sse"):
        load_transport_config()


def test_http_requires_token(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_transport_env(monkeypatch)
    monkeypatch.setenv("MEALIE_MCP_TRANSPORT", "http")
    with pytest.raises(ConfigError, match="MEALIE_MCP_HTTP_TOKEN"):
        load_transport_config()


def test_http_returns_configured_values(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_transport_env(monkeypatch)
    monkeypatch.setenv("MEALIE_MCP_TRANSPORT", "http")
    monkeypatch.setenv("MEALIE_MCP_HTTP_TOKEN", "secret")
    monkeypatch.setenv("MEALIE_MCP_HTTP_HOST", "0.0.0.0")  # noqa: S104
    monkeypatch.setenv("MEALIE_MCP_HTTP_PORT", "9001")
    monkeypatch.setenv("MEALIE_MCP_HTTP_ALLOWED_HOSTS", "mealie.example.com, , localhost")
    config = load_transport_config()
    assert config.transport == "http"
    assert config.auth_token == "secret"
    assert config.host == "0.0.0.0"  # noqa: S104
    assert config.port == 9001
    assert config.allowed_hosts == ("mealie.example.com", "localhost")


def test_http_defaults_when_only_token_set(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_transport_env(monkeypatch)
    monkeypatch.setenv("MEALIE_MCP_TRANSPORT", "http")
    monkeypatch.setenv("MEALIE_MCP_HTTP_TOKEN", "secret")
    config = load_transport_config()
    assert config.host == "127.0.0.1"
    assert config.port == 8000
    assert config.allowed_hosts == ("127.0.0.1", "localhost")


def test_http_rejects_unparsable_port(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_transport_env(monkeypatch)
    monkeypatch.setenv("MEALIE_MCP_TRANSPORT", "http")
    monkeypatch.setenv("MEALIE_MCP_HTTP_TOKEN", "secret")
    monkeypatch.setenv("MEALIE_MCP_HTTP_PORT", "notaport")
    with pytest.raises(ConfigError, match="MEALIE_MCP_HTTP_PORT"):
        load_transport_config()


@pytest.mark.parametrize("port", ["0", "-1", "99999"])
def test_http_rejects_out_of_range_port(monkeypatch: pytest.MonkeyPatch, port: str) -> None:
    _clear_transport_env(monkeypatch)
    monkeypatch.setenv("MEALIE_MCP_TRANSPORT", "http")
    monkeypatch.setenv("MEALIE_MCP_HTTP_TOKEN", "secret")
    monkeypatch.setenv("MEALIE_MCP_HTTP_PORT", port)
    with pytest.raises(ConfigError, match="between 1 and 65535"):
        load_transport_config()


def test_http_blank_allowed_hosts_falls_back_to_default(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_transport_env(monkeypatch)
    monkeypatch.setenv("MEALIE_MCP_TRANSPORT", "http")
    monkeypatch.setenv("MEALIE_MCP_HTTP_TOKEN", "secret")
    monkeypatch.setenv("MEALIE_MCP_HTTP_ALLOWED_HOSTS", "   ")
    config = load_transport_config()
    assert config.allowed_hosts == ("127.0.0.1", "localhost")
