"""Live test for the tag lifecycle.

Stages a sentinel tag, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import organizer_tags, recipe_crud


@pytest.fixture
def created_tag(mealie_client: AuthenticatedClient, sentinel_name: str) -> Iterator[dict[str, str]]:
    """Create a sentinel tag and ensure it is removed on teardown."""
    created = organizer_tags.create_tag(mealie_client, name=sentinel_name)
    item_id = created["id"]
    try:
        yield {"id": item_id, "name": sentinel_name}
    finally:
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=item_id)


@pytest.mark.live
def test_tag_lifecycle(mealie_client: AuthenticatedClient, created_tag: dict[str, str]) -> None:
    item_id = created_tag["id"]

    fetched = organizer_tags.get_tag(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == created_tag["name"]

    listing = organizer_tags.list_tags(mealie_client, search=created_tag["name"], per_page=100)
    assert any(t["id"] == item_id for t in listing["items"])

    matched = next(t for t in listing["items"] if t["id"] == item_id)
    by_slug = organizer_tags.get_tag_by_slug(mealie_client, slug=matched["slug"])
    assert by_slug["id"] == item_id

    updated_name = f"{created_tag['name']}-renamed"
    updated = organizer_tags.update_tag(mealie_client, item_id=item_id, name=updated_name)
    assert updated["id"] == item_id
    assert updated["name"] == updated_name

    ack = organizer_tags.delete_tag(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_tag failed \(404"):
        organizer_tags.get_tag(mealie_client, item_id=item_id)


@pytest.mark.live
def test_empty_tags_drops_a_tag_once_a_recipe_uses_it(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    tag = organizer_tags.create_tag(mealie_client, name=sentinel_name)
    tag_id = tag["id"]
    recipe_slug: str | None = None
    try:
        empty = organizer_tags.list_empty_tags(mealie_client)
        assert isinstance(empty, list)
        assert any(t["id"] == tag_id for t in empty)

        recipe_slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=recipe_slug,
            tags=[{"id": tag_id, "name": tag["name"], "slug": tag["slug"]}],
        )

        assert all(t["id"] != tag_id for t in organizer_tags.list_empty_tags(mealie_client))
    finally:
        if recipe_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe_slug)
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag_id)
