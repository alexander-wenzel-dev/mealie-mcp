"""Tests for the shared tool helpers."""

from __future__ import annotations

import json

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.tools._common import decode, raise_api_error, require_non_empty


class TestDecode:
    def test_empty_bytes_returns_none(self) -> None:
        assert decode(b"") is None

    def test_json_string(self) -> None:
        assert decode(b'"hello"') == "hello"

    def test_json_object(self) -> None:
        assert decode(b'{"k": 1}') == {"k": 1}

    def test_non_json_falls_back_to_utf8(self) -> None:
        assert decode(b"plain text") == "plain text"


class TestRaiseApiError:
    def test_dict_with_string_detail(self) -> None:
        body = json.dumps({"detail": "Recipe already exists"}).encode()
        with pytest.raises(ToolError, match=r"action failed \(409\): Recipe already exists"):
            raise_api_error("action", 409, body)

    def test_dict_with_message_fallback(self) -> None:
        body = json.dumps({"message": "boom"}).encode()
        with pytest.raises(ToolError, match=r"action failed \(500\): boom"):
            raise_api_error("action", 500, body)

    def test_dict_with_nested_detail(self) -> None:
        body = json.dumps({"detail": {"code": "x", "message": "y"}}).encode()
        with pytest.raises(ToolError) as excinfo:
            raise_api_error("action", 409, body)
        message = str(excinfo.value)
        assert "action failed (409):" in message
        assert json.loads(message.split("): ", 1)[1]) == {"code": "x", "message": "y"}

    def test_string_body(self) -> None:
        with pytest.raises(ToolError, match=r"action failed \(500\): upstream boom"):
            raise_api_error("action", 500, b"upstream boom")

    def test_empty_body_uses_status(self) -> None:
        with pytest.raises(ToolError, match=r"action failed \(502\): HTTP 502"):
            raise_api_error("action", 502, b"")


class TestRequireNonEmpty:
    def test_rejects_empty_string(self) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            require_non_empty("name", "")

    def test_rejects_whitespace(self) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            require_non_empty("name", "   ")

    def test_accepts_value(self) -> None:
        require_non_empty("name", "x")
