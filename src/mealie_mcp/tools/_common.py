"""Shared helpers used by tool modules."""

from __future__ import annotations

import json
from typing import Any

from fastmcp.exceptions import ToolError


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
