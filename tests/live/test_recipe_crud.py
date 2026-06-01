"""Live tests for the recipe CRUD lifecycle.

Each test stages a sentinel recipe (or another sentinel artifact) with the
shared fixtures, exercises a tool, asserts on the observable effect, and tears
the sentinel down even when the body fails.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import json
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_crud


@pytest.fixture
def created_recipe(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel recipe and ensure it is removed on teardown."""
    created = recipe_crud.create_recipe(mealie_client, name=sentinel_name)
    try:
        yield {"slug": created["slug"], "name": sentinel_name}
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=created["slug"])


@pytest.mark.live
def test_recipe_crud_lifecycle(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    slug = created_recipe["slug"]

    fetched = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert fetched["slug"] == slug
    assert fetched["name"] == created_recipe["name"]

    recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)

    with pytest.raises(ToolError, match=r"get_recipe failed \(404"):
        recipe_crud.get_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_list_recipes_includes_sentinel(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    listing = recipe_crud.list_recipes(mealie_client, search=created_recipe["name"], per_page=100)
    assert any(item["slug"] == created_recipe["slug"] for item in listing["items"])


@pytest.mark.live
def test_duplicate_recipe_creates_new_slug(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    duplicate_name = f"{sentinel_name}-dup"
    duplicate = recipe_crud.duplicate_recipe(
        mealie_client, slug_or_id=created_recipe["slug"], name=duplicate_name
    )
    try:
        assert duplicate["slug"] != created_recipe["slug"]
        assert duplicate["name"] == duplicate_name
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=duplicate["slug"])


@pytest.mark.live
def test_update_last_made_persists_timestamp(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    timestamp = dt.datetime(2026, 6, 1, 12, 0, 0, tzinfo=dt.UTC).isoformat()
    recipe_crud.update_last_made(
        mealie_client, slug_or_id=created_recipe["slug"], timestamp=timestamp
    )
    refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=created_recipe["slug"])
    assert refreshed["lastMade"] is not None


@pytest.mark.live
def test_create_recipe_from_html_or_json(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    json_ld = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": sentinel_name,
        "recipeIngredient": ["1 cup flour", "2 eggs"],
        "recipeInstructions": [{"@type": "HowToStep", "text": "Mix and bake."}],
    }
    result = recipe_crud.create_recipe_from_html_or_json(mealie_client, data=json.dumps(json_ld))
    slug = result["slug"]
    try:
        fetched = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        assert fetched["slug"] == slug
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_parse_recipe_url_rejects_invalid_url(mealie_client: AuthenticatedClient) -> None:
    with pytest.raises(ToolError, match=r"parse_recipe_url failed"):
        recipe_crud.parse_recipe_url(mealie_client, url="https://example.com/not-a-recipe")
