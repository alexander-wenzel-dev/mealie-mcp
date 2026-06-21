"""Recipe timeline event tools.

Mirrors `mealie_mcp.client.api.recipe_timeline`. Exposes the recipe cooking
journal: list a recipe's events, create, read, update, and delete an event.

Timeline events reference their recipe by UUID, not slug. The recipe-scoped
list builds Mealie's generic ``queryFilter`` from that id. Create sets
``event_type`` once; it is immutable afterwards, so update never touches it.
"""

from __future__ import annotations

import datetime as dt
from http import HTTPStatus
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipe_timeline import (
    create_one_api_recipes_timeline_events_post,
    delete_one_api_recipes_timeline_events_item_id_delete,
    get_all_api_recipes_timeline_events_get,
    get_one_api_recipes_timeline_events_item_id_get,
    update_one_api_recipes_timeline_events_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.recipe_timeline_event_in import RecipeTimelineEventIn
from mealie_mcp.client.models.recipe_timeline_event_update import RecipeTimelineEventUpdate
from mealie_mcp.client.models.timeline_event_type import TimelineEventType
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    require_non_empty,
    require_per_page,
    to_unset,
)

CREATABLE_EVENT_TYPES = ("comment", "info")


def _parse_event_type(value: str) -> TimelineEventType:
    """Coerce a caller's event type into the enum, rejecting anything but the creatable set.

    Mealie's ``system`` events are server generated and out of scope, so the
    tool refuses to create them even though the enum carries the value.
    """
    if value not in CREATABLE_EVENT_TYPES:
        allowed = " or ".join(repr(t) for t in CREATABLE_EVENT_TYPES)
        raise ToolError(f"event_type must be {allowed} (got {value!r})")
    return TimelineEventType(value)


def _parse_timestamp(value: str) -> dt.datetime:
    """Parse a caller's ISO 8601 timestamp into a datetime or raise `ToolError`."""
    try:
        return dt.datetime.fromisoformat(value)
    except ValueError as exc:
        raise ToolError(f"timestamp must be an ISO 8601 datetime: {exc}") from exc


def list_recipe_timeline_events(
    client: AuthenticatedClient, recipe_id: str, page: int = 1, per_page: int = 50
) -> dict[str, Any]:
    """List a recipe's timeline events, paginated. Returns the pagination envelope."""
    require_non_empty("recipe_id", recipe_id)
    require_per_page(per_page)

    response = get_all_api_recipes_timeline_events_get.sync_detailed(
        client=client,
        query_filter=f'recipe_id="{recipe_id}"',
        page=page,
        per_page=per_page,
    )
    return expect_dict("list_recipe_timeline_events", response)


def create_timeline_event(
    client: AuthenticatedClient,
    recipe_id: str,
    subject: str,
    event_type: str = "info",
    event_message: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Create a timeline event on a recipe. Returns the new event payload."""
    require_non_empty("recipe_id", recipe_id)
    require_non_empty("subject", subject)
    parsed_type = _parse_event_type(event_type)
    parsed_timestamp = _parse_timestamp(timestamp) if timestamp is not None else None

    body = RecipeTimelineEventIn(
        recipe_id=recipe_id,
        subject=subject,
        event_type=parsed_type,
        event_message=to_unset(event_message),
        timestamp=to_unset(parsed_timestamp),
    )
    response = create_one_api_recipes_timeline_events_post.sync_detailed(client=client, body=body)
    return expect_dict("create_timeline_event", response, HTTPStatus.CREATED)


def get_timeline_event(client: AuthenticatedClient, event_id: str) -> dict[str, Any]:
    """Fetch a timeline event by id. Returns the event payload."""
    require_non_empty("event_id", event_id)

    response = get_one_api_recipes_timeline_events_item_id_get.sync_detailed(
        event_id, client=client
    )
    return expect_dict("get_timeline_event", response)


def update_timeline_event(
    client: AuthenticatedClient,
    event_id: str,
    subject: str | None = None,
    event_message: str | None = None,
) -> dict[str, Any]:
    """Update a timeline event's subject or message. Returns the updated event payload.

    The update endpoint requires ``subject`` and PUT-replaces the body fields,
    so a message-only edit still has to resend the current subject. The tool
    fetches the event and applies whichever fields the caller set, leaving the
    rest to round-trip from the stored event.
    """
    require_non_empty("event_id", event_id)
    if subject is None and event_message is None:
        raise ToolError("update_timeline_event requires subject or event_message")
    if subject is not None:
        require_non_empty("subject", subject)

    prefetch = get_one_api_recipes_timeline_events_item_id_get.sync_detailed(
        event_id, client=client
    )
    existing = expect_dict("update_timeline_event", prefetch)
    try:
        body = RecipeTimelineEventUpdate.from_dict(existing)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ToolError(f"Mealie update_timeline_event failed: {exc}") from exc
    body.additional_properties = {}
    if subject is not None:
        body.subject = subject
    if event_message is not None:
        body.event_message = event_message

    response = update_one_api_recipes_timeline_events_item_id_put.sync_detailed(
        event_id, client=client, body=body
    )
    return expect_dict("update_timeline_event", response)


def delete_timeline_event(client: AuthenticatedClient, event_id: str) -> dict[str, Any]:
    """Delete a timeline event by id. Returns ``{"id": event_id, "deleted": True}``."""
    require_non_empty("event_id", event_id)

    response = delete_one_api_recipes_timeline_events_item_id_delete.sync_detailed(
        event_id, client=client
    )
    return ack_delete("delete_timeline_event", response, event_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the recipe timeline tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_recipe_timeline_events")
    def _list_recipe_timeline_events(
        recipe_id: str, page: int = 1, per_page: int = 50
    ) -> dict[str, Any]:
        """List the timeline events attached to a single recipe, paginated.

        Args:
            recipe_id: UUID of the recipe whose events to list.
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50. Capped at 100.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_recipe_timeline_events(
            get_client(), recipe_id=recipe_id, page=page, per_page=per_page
        )

    @mcp.tool(name="mealie_create_timeline_event")
    def _create_timeline_event(
        recipe_id: str,
        subject: str,
        event_type: str = "info",
        event_message: str | None = None,
        timestamp: str | None = None,
    ) -> dict[str, Any]:
        """Create a timeline event on a Mealie recipe.

        Args:
            recipe_id: UUID of the recipe to log against.
            subject: Event title. Required, must be non-empty.
            event_type: ``"comment"`` or ``"info"``. Defaults to ``"info"``.
                ``"system"`` events are server generated and rejected.
            event_message: Optional event body.
            timestamp: Optional ISO 8601 datetime. Defaults to the server's
                current time when omitted.

        Returns:
            The newly created event payload as a JSON-compatible dict.
        """
        return create_timeline_event(
            get_client(),
            recipe_id=recipe_id,
            subject=subject,
            event_type=event_type,
            event_message=event_message,
            timestamp=timestamp,
        )

    @mcp.tool(name="mealie_get_timeline_event")
    def _get_timeline_event(event_id: str) -> dict[str, Any]:
        """Fetch a single timeline event from Mealie by id.

        Args:
            event_id: UUID of the timeline event.

        Returns:
            The event payload as a JSON-compatible dict.
        """
        return get_timeline_event(get_client(), event_id=event_id)

    @mcp.tool(name="mealie_update_timeline_event")
    def _update_timeline_event(
        event_id: str,
        subject: str | None = None,
        event_message: str | None = None,
    ) -> dict[str, Any]:
        """Update the subject or message of an existing timeline event.

        The event type and timestamp are fixed at create time and cannot be
        changed. Pass at least one of ``subject`` or ``event_message``.

        Args:
            event_id: UUID of the event to update.
            subject: New event title. Omit to keep the current title.
            event_message: New event body. Omit to keep the current body.

        Returns:
            The updated event payload as a JSON-compatible dict.
        """
        return update_timeline_event(
            get_client(), event_id=event_id, subject=subject, event_message=event_message
        )

    @mcp.tool(name="mealie_delete_timeline_event")
    def _delete_timeline_event(event_id: str) -> dict[str, Any]:
        """Delete a timeline event from Mealie by id.

        Args:
            event_id: UUID of the event to delete.

        Returns:
            A canonical acknowledgement ``{"id": <event_id>, "deleted": True}``.
        """
        return delete_timeline_event(get_client(), event_id=event_id)
