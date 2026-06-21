"""Live test for the recipe timeline event lifecycle.

Stages a sentinel recipe, attaches a sentinel timeline event, exercises read,
recipe-scoped list, update, and delete, then tears both sentinels down. A
second recipe with its own event proves the list `queryFilter` actually scopes
to one recipe. Cleanup runs even when the test body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

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

    refetched = recipe_timeline.get_timeline_event(mealie_client, event_id=event_id)
    assert refetched["eventMessage"] == new_message
    assert refetched["subject"] == created_event["subject"]

    ack = recipe_timeline.delete_timeline_event(mealie_client, event_id=event_id)
    assert ack == {"id": event_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_timeline_event failed \(404"):
        recipe_timeline.get_timeline_event(mealie_client, event_id=event_id)
