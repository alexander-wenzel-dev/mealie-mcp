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
from mealie_mcp.tools import organizer_categories, organizer_tags, recipe_crud


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

    ack = recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
    assert ack == {"id": slug, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_recipe failed \(404"):
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
def test_update_recipe_patches_scalars_and_lists(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    slug = created_recipe["slug"]
    updated = recipe_crud.update_recipe(
        mealie_client,
        slug_or_id=slug,
        description="updated by mcp-test",
        recipe_yield="6 servings",
        total_time="55 minutes",
        prep_time="15 minutes",
        perform_time="40 minutes",
        recipe_ingredient=[{"note": "1 cup flour"}, {"note": "2 eggs"}],
        notes=[{"title": "mcp", "text": "patched note"}],
        recipe_instructions=[{"text": "Step one."}, {"text": "Step two."}],
    )
    assert updated["slug"] == slug
    assert updated["description"] == "updated by mcp-test"

    refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert refreshed["description"] == "updated by mcp-test"
    assert refreshed["recipeYield"] == "6 servings"
    assert refreshed["totalTime"] == "55 minutes"
    assert refreshed["prepTime"] == "15 minutes"
    assert refreshed["performTime"] == "40 minutes"
    assert [ing["note"] for ing in refreshed["recipeIngredient"]] == [
        "1 cup flour",
        "2 eggs",
    ]
    assert [note["text"] for note in refreshed["notes"]] == ["patched note"]
    assert [step["text"] for step in refreshed["recipeInstructions"]] == [
        "Step one.",
        "Step two.",
    ]


@pytest.mark.live
def test_update_recipe_reslugs_on_name_change(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    new_name = f"{sentinel_name}-renamed"
    updated = recipe_crud.update_recipe(
        mealie_client, slug_or_id=created_recipe["slug"], name=new_name
    )
    new_slug = updated["slug"]
    try:
        assert new_slug != created_recipe["slug"]
        assert updated["name"] == new_name
        refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=new_slug)
        assert refreshed["name"] == new_name
    finally:
        # The recipe lives at the new slug now; the fixture's cleanup at the
        # original slug is a 404 no-op suppressed by its contextlib.suppress.
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=new_slug)


@pytest.mark.live
def test_update_recipe_attaches_tag_and_category(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    tag = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-tag")
    category = organizer_categories.create_category(mealie_client, name=f"{sentinel_name}-cat")
    try:
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=created_recipe["slug"],
            tags=[{"id": tag["id"], "name": tag["name"], "slug": tag["slug"]}],
            recipe_category=[
                {"id": category["id"], "name": category["name"], "slug": category["slug"]}
            ],
        )
        refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=created_recipe["slug"])
        assert [t["slug"] for t in refreshed["tags"]] == [tag["slug"]]
        assert [c["slug"] for c in refreshed["recipeCategory"]] == [category["slug"]]
    finally:
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag["id"])
        with contextlib.suppress(ToolError):
            organizer_categories.delete_category(mealie_client, item_id=category["id"])


@pytest.mark.live
def test_update_last_made_persists_timestamp(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    sent = dt.datetime(2026, 6, 1, 12, 0, 0, tzinfo=dt.UTC)
    recipe_crud.update_last_made(
        mealie_client, slug_or_id=created_recipe["slug"], timestamp=sent.isoformat()
    )
    refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=created_recipe["slug"])
    returned_iso = refreshed["lastMade"]
    assert returned_iso is not None
    returned = dt.datetime.fromisoformat(returned_iso)
    if returned.tzinfo is None:
        returned = returned.replace(tzinfo=dt.UTC)
    assert returned.replace(microsecond=0) == sent


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
    with pytest.raises(ToolError, match=r"Mealie parse_recipe_url failed"):
        recipe_crud.parse_recipe_url(mealie_client, url="https://example.com/not-a-recipe")
