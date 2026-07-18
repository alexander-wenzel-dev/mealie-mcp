"""Live test for the category lifecycle.

Stages a sentinel category, exercises the read, list, update, and delete
tools, and tears the sentinel down even when the body fails so no
`mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import organizer_categories, recipe_crud


@pytest.fixture
def created_category(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel category and ensure it is removed on teardown."""
    created = organizer_categories.create_category(mealie_client, name=sentinel_name)
    item_id = created["id"]
    try:
        yield {"id": item_id, "name": sentinel_name}
    finally:
        with contextlib.suppress(ToolError):
            organizer_categories.delete_category(mealie_client, item_id=item_id)


@pytest.mark.live
def test_category_lifecycle(
    mealie_client: AuthenticatedClient, created_category: dict[str, str]
) -> None:
    item_id = created_category["id"]

    fetched = organizer_categories.get_category(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == created_category["name"]

    listing = organizer_categories.list_categories(
        mealie_client, search=created_category["name"], per_page=100
    )
    assert any(c["id"] == item_id for c in listing["items"])

    matched = next(c for c in listing["items"] if c["id"] == item_id)
    by_slug = organizer_categories.get_category_by_slug(mealie_client, slug=matched["slug"])
    assert by_slug["id"] == item_id

    updated_name = f"{created_category['name']}-renamed"
    updated = organizer_categories.update_category(
        mealie_client, item_id=item_id, name=updated_name
    )
    assert updated["id"] == item_id
    assert updated["name"] == updated_name

    ack = organizer_categories.delete_category(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_category failed \(404"):
        organizer_categories.get_category(mealie_client, item_id=item_id)


@pytest.mark.live
def test_empty_categories_drops_a_category_once_a_recipe_uses_it(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    category = organizer_categories.create_category(mealie_client, name=sentinel_name)
    category_id = category["id"]
    recipe_slug: str | None = None
    try:
        empty = organizer_categories.list_empty_categories(mealie_client)
        assert isinstance(empty, list)
        assert any(c["id"] == category_id for c in empty)

        recipe_slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=recipe_slug,
            recipe_category=[
                {"id": category_id, "name": category["name"], "slug": category["slug"]}
            ],
        )

        assert all(
            c["id"] != category_id
            for c in organizer_categories.list_empty_categories(mealie_client)
        )
    finally:
        if recipe_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe_slug)
        with contextlib.suppress(ToolError):
            organizer_categories.delete_category(mealie_client, item_id=category_id)


@pytest.mark.live
def test_get_category_by_id_omits_recipes_while_by_slug_hydrates(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    category = organizer_categories.create_category(mealie_client, name=sentinel_name)
    category_id = category["id"]
    recipe_slug: str | None = None
    try:
        recipe_slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=recipe_slug,
            recipe_category=[
                {"id": category_id, "name": category["name"], "slug": category["slug"]}
            ],
        )

        # The by-id read returns a compact payload with no recipes list.
        by_id = organizer_categories.get_category(mealie_client, item_id=category_id)
        assert "recipes" not in by_id

        # The by-slug read hydrates recipes, including the one just attached.
        by_slug = organizer_categories.get_category_by_slug(mealie_client, slug=category["slug"])
        assert any(r["slug"] == recipe_slug for r in by_slug["recipes"])
    finally:
        if recipe_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe_slug)
        with contextlib.suppress(ToolError):
            organizer_categories.delete_category(mealie_client, item_id=category_id)
