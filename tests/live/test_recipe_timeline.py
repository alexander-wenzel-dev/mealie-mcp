"""Live test for the recipe timeline event lifecycle.

Stages a sentinel recipe, attaches a sentinel timeline event, exercises read,
recipe-scoped list, update, and delete, then tears both sentinels down. A
second recipe with its own event proves the list `queryFilter` actually scopes
to one recipe. Cleanup runs even when the test body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
import datetime as dt
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_crud, recipe_timeline


@pytest.fixture
def created_recipe(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a parent recipe so timeline events have something to attach to."""
    created = recipe_crud.create_recipe(mealie_client, name=sentinel_name)
    slug = created["slug"]
    try:
        recipe = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        yield {"slug": slug, "id": recipe["id"]}
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.fixture
def created_event(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Attach a sentinel timeline event to the parent recipe and tear it down."""
    subject = f"{sentinel_name}-subject"
    message = f"{sentinel_name}-message"
    created = recipe_timeline.create_timeline_event(
        mealie_client,
        recipe_id=created_recipe["id"],
        subject=subject,
        event_type="info",
        event_message=message,
    )
    event_id = created["id"]
    try:
        yield {"id": event_id, "subject": subject, "message": message}
    finally:
        with contextlib.suppress(ToolError):
            recipe_timeline.delete_timeline_event(mealie_client, event_id=event_id)


@pytest.mark.live
def test_recipe_timeline_event_lifecycle(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    created_event: dict[str, str],
    sentinel_name: str,
) -> None:
    event_id = created_event["id"]
    recipe_id = created_recipe["id"]

    fetched = recipe_timeline.get_timeline_event(mealie_client, event_id=event_id)
    assert fetched["id"] == event_id
    assert fetched["subject"] == created_event["subject"]
    assert fetched["eventMessage"] == created_event["message"]
    assert fetched["recipeId"] == recipe_id

    # A second recipe with its own event proves the list filter scopes by recipe.
    other = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-other")
    other_slug = other["slug"]
    try:
        other_recipe = recipe_crud.get_recipe(mealie_client, slug_or_id=other_slug)
        other_event = recipe_timeline.create_timeline_event(
            mealie_client,
            recipe_id=other_recipe["id"],
            subject=f"{sentinel_name}-other-subject",
            event_type="info",
        )
        other_event_id = other_event["id"]

        listing = recipe_timeline.list_recipe_timeline_events(
            mealie_client, recipe_id=recipe_id, per_page=100
        )
        ids = {item["id"] for item in listing["items"]}
        assert event_id in ids
        assert other_event_id not in ids
        assert all(item["recipeId"] == recipe_id for item in listing["items"])
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=other_slug)

    # Update only the message; the original subject must survive the PUT-replace.
    new_message = f"{sentinel_name}-message-updated"
    updated = recipe_timeline.update_timeline_event(
        mealie_client, event_id=event_id, event_message=new_message
    )
    assert updated["id"] == event_id
    assert updated["eventMessage"] == new_message
    assert updated["subject"] == created_event["subject"]
    # event_type is immutable and absent from the update model, so it must
    # survive a message-only edit rather than reset under the PUT-replace.
    assert updated["eventType"] == "info"

    refetched = recipe_timeline.get_timeline_event(mealie_client, event_id=event_id)
    assert refetched["eventMessage"] == new_message
    assert refetched["subject"] == created_event["subject"]

    ack = recipe_timeline.delete_timeline_event(mealie_client, event_id=event_id)
    assert ack == {"id": event_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_timeline_event failed \(404"):
        recipe_timeline.get_timeline_event(mealie_client, event_id=event_id)


def _event_order(listing: dict[str, Any], *ids: str) -> list[str]:
    """The given event ids in the order they appear in a timeline listing.

    Keys on the known ids so the recipe's auto-created `system` event and any
    other events do not affect the result. Asserts both ids are present before
    reporting their order.
    """
    items = listing["items"]
    assert isinstance(items, list)
    positions = {item["id"]: index for index, item in enumerate(items)}
    for event_id in ids:
        assert event_id in positions, f"event {event_id} not found in listing"
    return sorted(ids, key=lambda event_id: positions[event_id])


@pytest.mark.live
def test_list_recipe_timeline_events_order_direction_flips_relative_order(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
) -> None:
    """``order_direction`` reverses the relative order of two events by timestamp.

    Two events are staged with distinct explicit timestamps. Listing ascending
    then descending by ``timestamp`` must flip their relative order. The
    assertion keys on the two known ids so the recipe's auto-created `system`
    event does not affect it.
    """
    recipe_id = created_recipe["id"]
    earlier = recipe_timeline.create_timeline_event(
        mealie_client,
        recipe_id=recipe_id,
        subject=f"{sentinel_name}-earlier",
        event_type="info",
        timestamp="2020-01-01T00:00:00",
    )
    later = recipe_timeline.create_timeline_event(
        mealie_client,
        recipe_id=recipe_id,
        subject=f"{sentinel_name}-later",
        event_type="info",
        timestamp="2020-06-01T00:00:00",
    )
    try:
        ascending = _event_order(
            recipe_timeline.list_recipe_timeline_events(
                mealie_client,
                recipe_id=recipe_id,
                per_page=100,
                order_by="timestamp",
                order_direction="asc",
            ),
            earlier["id"],
            later["id"],
        )
        descending = _event_order(
            recipe_timeline.list_recipe_timeline_events(
                mealie_client,
                recipe_id=recipe_id,
                per_page=100,
                order_by="timestamp",
                order_direction="desc",
            ),
            earlier["id"],
            later["id"],
        )
        assert ascending == [earlier["id"], later["id"]]
        assert descending == [later["id"], earlier["id"]]
    finally:
        for event_id in (earlier["id"], later["id"]):
            with contextlib.suppress(ToolError):
                recipe_timeline.delete_timeline_event(mealie_client, event_id=event_id)


@pytest.mark.live
def test_create_timeline_event_round_trips_through_wrapper(
    created_recipe: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    subject = f"{sentinel_name}-subject"
    created = call_tool(
        "mealie_create_timeline_event",
        {"recipe_id": created_recipe["id"], "subject": subject},
    )
    assert isinstance(created, dict)
    event_id = created["id"]
    try:
        assert created["subject"] == subject
        assert created["recipeId"] == created_recipe["id"]
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_timeline_event", {"event_id": event_id})


def _parse_utc(value: str) -> dt.datetime:
    """Parse an ISO 8601 timestamp and normalize it to a UTC-aware datetime."""
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt.UTC)
    return parsed.astimezone(dt.UTC)


@pytest.mark.live
def test_create_timeline_event_omitted_timestamp_stamps_current_time(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
) -> None:
    """An omitted timestamp is stamped near now, not with the server boot time.

    Mealie's schema default for the timestamp is evaluated once at server
    import, so an UNSET timestamp lands at the server boot time, which can be
    days old. The tool sends the current time explicitly to avoid that, so the
    returned timestamp must sit within a small window of now.
    """
    before = dt.datetime.now(dt.UTC)
    created = recipe_timeline.create_timeline_event(
        mealie_client,
        recipe_id=created_recipe["id"],
        subject=f"{sentinel_name}-subject",
        event_type="info",
    )
    after = dt.datetime.now(dt.UTC)
    event_id = created["id"]
    try:
        stamped = _parse_utc(created["timestamp"])
        assert before - dt.timedelta(seconds=5) <= stamped <= after + dt.timedelta(seconds=5)
    finally:
        with contextlib.suppress(ToolError):
            recipe_timeline.delete_timeline_event(mealie_client, event_id=event_id)
