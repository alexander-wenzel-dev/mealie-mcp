"""Shared helpers used by tool modules."""

from __future__ import annotations

import json
from http import HTTPStatus
from typing import Any

from fastmcp.exceptions import ToolError

from mealie_mcp.client.types import Response


def decode(content: bytes) -> Any:
    """Best effort decode of an httpx response body to a JSON value or string."""
    if not content:
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return content.decode("utf-8", errors="replace")


def raise_api_error(action: str, status: int, content: bytes) -> None:
    """Raise a `ToolError` that preserves the Mealie error message."""
    body = decode(content)
    if isinstance(body, dict):
        detail = body.get("detail") or body.get("message") or body
        message = detail if isinstance(detail, str) else json.dumps(detail)
    elif isinstance(body, str):
        message = body
    else:
        message = f"HTTP {status}"
    raise ToolError(f"Mealie {action} failed ({status}): {message}")


def require_non_empty(name: str, value: str) -> None:
    """Raise a `ToolError` if `value` is empty or whitespace."""
    if not value or not value.strip():
        raise ToolError(f"{name} must be a non-empty string")


def _expect(action: str, response: Response[Any], status: HTTPStatus) -> Any:
    if response.status_code != status:
        raise_api_error(action, int(response.status_code), response.content)
    return decode(response.content)


def expect_dict(
    action: str, response: Response[Any], status: HTTPStatus = HTTPStatus.OK
) -> dict[str, Any]:
    """Return the response body as a dict or raise `ToolError`."""
    payload = _expect(action, response, status)
    if not isinstance(payload, dict):
        raise ToolError(f"Unexpected {action} response: {payload!r}")
    return payload


def expect_list(
    action: str, response: Response[Any], status: HTTPStatus = HTTPStatus.OK
) -> list[Any]:
    """Return the response body as a list or raise `ToolError`."""
    payload = _expect(action, response, status)
    if not isinstance(payload, list):
        raise ToolError(f"Unexpected {action} response: {payload!r}")
    return payload


def expect_str(action: str, response: Response[Any], status: HTTPStatus = HTTPStatus.OK) -> str:
    """Return the response body as a string or raise `ToolError`."""
    payload = _expect(action, response, status)
    if not isinstance(payload, str):
        raise ToolError(f"Unexpected {action} response: {payload!r}")
    return payload
