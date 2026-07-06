"""Shared helpers used by tool modules."""

from __future__ import annotations

import json
from http import HTTPStatus
from typing import Any
from uuid import UUID

from fastmcp.exceptions import ToolError

from mealie_mcp.client.models.order_direction import OrderDirection
from mealie_mcp.client.types import UNSET, Response, Unset


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


MAX_PER_PAGE = 100


def require_pagination(page: int, per_page: int) -> None:
    """Raise a `ToolError` if the pagination window is outside the supported range.

    `per_page` is bounded to `1..MAX_PER_PAGE` on both sides. The ceiling caps
    tool output size; the floor stops the two broken low values Mealie accepts,
    `-1` (an unbounded "all rows" fetch that defeats the ceiling) and `0` (an
    empty page). `page` is bounded to `>= 1` for the same reason: Mealie
    silently coerces `0` to page 1 and reads a negative page as the last page,
    so an out-of-range value returns a surprising result instead of an error.
    """
    if page < 1:
        raise ToolError(f"page must be >= 1 (got {page})")
    if per_page < 1 or per_page > MAX_PER_PAGE:
        raise ToolError(f"per_page must be between 1 and {MAX_PER_PAGE} (got {per_page})")


def to_unset[T](value: T | None) -> T | Unset:
    """Translate a caller's optional value into the generated client's UNSET sentinel.

    `None` would otherwise serialise as JSON ``null``, which Mealie rejects on
    most query parameters. Non-`None` values pass through unchanged.
    """
    if value is None:
        return UNSET
    return value


def ack_delete(action: str, response: Response[Any], ack_id: str) -> dict[str, Any]:
    """Return the canonical delete acknowledgement after verifying a 200 response.

    The MCP tool contract for every ``mealie_delete_*`` is the same shape
    regardless of what Mealie chose to return in the body, so callers can rely
    on a stable output across endpoints.
    """
    if response.status_code != HTTPStatus.OK:
        raise_api_error(action, int(response.status_code), response.content)
    return {"id": ack_id, "deleted": True}


def parse_recipe_uuid(value: str) -> UUID:
    """Parse a recipe id into a UUID or raise `ToolError`."""
    try:
        return UUID(value)
    except ValueError as exc:
        raise ToolError(f"recipe_id must be a recipe UUID: {exc}") from exc


def parse_order_direction(value: str | None) -> OrderDirection | Unset:
    """Coerce a caller-supplied 'asc'/'desc' into the typed enum."""
    if value is None:
        return UNSET
    try:
        return OrderDirection(value)
    except ValueError as exc:
        raise ToolError(f"order_direction must be 'asc' or 'desc': {exc}") from exc


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
