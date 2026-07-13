"""Live tests for the recipe bulk-action tools.

Each test stages at least two sentinel recipes so every action is proven across
the whole set rather than a single recipe, exercises a bulk tool, asserts the
observable effect on each recipe, and tears the sentinels down even when the
body fails.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipe_crud import patch_one_api_recipes_slug_patch
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.recipe import Recipe
from mealie_mcp.tools import organizer_categories, organizer_tags, recipe_bulk_actions, recipe_crud
from mealie_mcp.tools._common import expect_dict


def _full_object(item: dict[str, str]) -> dict[str, str]:
    """A tag or category as the bulk endpoints expect it: a full object."""
    return {"id": item["id"], "name": item["name"], "slug": item["slug"]}


def _lock_recipe(client: AuthenticatedClient, slug: str) -> None:
    """Set locked on a recipe's settings and confirm the lock took."""
    settings = recipe_crud.get_recipe(client, slug_or_id=slug)["settings"]
    settings["locked"] = True
    updated = expect_dict(
        "lock_recipe",
        patch_one_api_recipes_slug_patch.sync_detailed(
            slug, client=client, body=Recipe.from_dict({"settings": settings})
        ),
    )
    assert updated["settings"]["locked"] is True, "staging failed to lock the recipe"


@pytest.fixture
def two_recipe_slugs(mealie_client: AuthenticatedClient, sentinel_name: str) -> Iterator[list[str]]:
    """Create two sentinel recipes and remove both on teardown."""
    slugs = [
        recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-{n}")["slug"]
        for n in ("one", "two")
    ]
    try:
        yield slugs
    finally:
        for slug in slugs:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_tag_recipes_tags_every_recipe(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str], sentinel_name: str
) -> None:
    tag = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-tag")
    try:
        ack = recipe_bulk_actions.tag_recipes(
            mealie_client, recipes=two_recipe_slugs, tags=[_full_object(tag)]
        )
        assert ack == {"recipes": two_recipe_slugs, "tagged": True}

        for slug in two_recipe_slugs:
            refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
            assert tag["slug"] in [t["slug"] for t in refreshed["tags"]]
    finally:
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag["id"])


@pytest.mark.live
def test_tag_recipes_is_additive(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str], sentinel_name: str
) -> None:
    first = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-first")
    second = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-second")
    try:
        recipe_bulk_actions.tag_recipes(
            mealie_client, recipes=two_recipe_slugs, tags=[_full_object(first)]
        )
        recipe_bulk_actions.tag_recipes(
            mealie_client, recipes=two_recipe_slugs, tags=[_full_object(second)]
        )
        for slug in two_recipe_slugs:
            refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
            slugs = {t["slug"] for t in refreshed["tags"]}
            assert {first["slug"], second["slug"]} <= slugs
    finally:
        for tag in (first, second):
            with contextlib.suppress(ToolError):
                organizer_tags.delete_tag(mealie_client, item_id=tag["id"])


@pytest.mark.live
def test_categorize_recipes_categorizes_every_recipe(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str], sentinel_name: str
) -> None:
    category = organizer_categories.create_category(mealie_client, name=f"{sentinel_name}-cat")
    try:
        ack = recipe_bulk_actions.categorize_recipes(
            mealie_client, recipes=two_recipe_slugs, categories=[_full_object(category)]
        )
        assert ack == {"recipes": two_recipe_slugs, "categorized": True}

        for slug in two_recipe_slugs:
            refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
            assert category["slug"] in [c["slug"] for c in refreshed["recipeCategory"]]
    finally:
        with contextlib.suppress(ToolError):
            organizer_categories.delete_category(mealie_client, item_id=category["id"])


@pytest.mark.live
def test_apply_recipe_settings_sets_values_on_every_recipe(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str]
) -> None:
    # A new recipe defaults public, showNutrition, showAssets, and landscapeView
    # to false and disableComments to true, so flipping every exposed field is an
    # observable change on each recipe. locked is not asserted here: the endpoint
    # preserves each recipe's existing lock state, proven in its own test.
    ack = recipe_bulk_actions.apply_recipe_settings(
        mealie_client,
        recipes=two_recipe_slugs,
        public=True,
        show_nutrition=True,
        show_assets=True,
        landscape_view=True,
        disable_comments=False,
    )
    assert ack == {"recipes": two_recipe_slugs, "settings_applied": True}

    for slug in two_recipe_slugs:
        settings = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["settings"]
        assert settings["public"] is True
        assert settings["showNutrition"] is True
        assert settings["showAssets"] is True
        assert settings["landscapeView"] is True
        assert settings["disableComments"] is False


@pytest.mark.live
def test_apply_recipe_settings_preserves_lock_state(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str]
) -> None:
    # RecipeSettings carries locked, which the tool does not expose, and the
    # endpoint replaces the settings object wholesale. Lock one sentinel, then
    # apply settings across both and assert the lock survived: the bulk endpoint
    # keeps each recipe's existing lock state rather than resetting it to the
    # default the tool sends. Without this the tool would silently unlock.
    locked_slug = two_recipe_slugs[0]
    _lock_recipe(mealie_client, locked_slug)

    recipe_bulk_actions.apply_recipe_settings(
        mealie_client,
        recipes=two_recipe_slugs,
        public=True,
        show_nutrition=True,
        show_assets=False,
        landscape_view=True,
        disable_comments=False,
    )

    settings = recipe_crud.get_recipe(mealie_client, slug_or_id=locked_slug)["settings"]
    assert settings["locked"] is True
    assert settings["public"] is True


@pytest.mark.live
def test_delete_recipes_removes_every_recipe(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str]
) -> None:
    ack = recipe_bulk_actions.delete_recipes(mealie_client, recipes=two_recipe_slugs)
    assert ack == {"ids": two_recipe_slugs, "deleted": True}

    for slug in two_recipe_slugs:
        with pytest.raises(ToolError, match=r"Mealie get_recipe failed \(404"):
            recipe_crud.get_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_tag_recipes_missing_slug_raises_and_still_mutates_valid(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str], sentinel_name: str
) -> None:
    # Partial-failure probe for the tag/categorize/settings family: a nonexistent
    # slug makes the endpoint return 500, so the tool raises. The valid recipe is
    # still mutated before the missing one is reached, so a partial failure is
    # not silent but leaves the batch half-applied.
    valid = two_recipe_slugs[0]
    tag = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-tag")
    try:
        with pytest.raises(ToolError, match=r"Mealie tag_recipes failed \(500"):
            recipe_bulk_actions.tag_recipes(
                mealie_client,
                recipes=[valid, f"{sentinel_name}-missing"],
                tags=[_full_object(tag)],
            )
        refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=valid)
        assert tag["slug"] in [t["slug"] for t in refreshed["tags"]]
    finally:
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag["id"])


@pytest.mark.live
def test_delete_recipes_skips_missing_slug(
    mealie_client: AuthenticatedClient, two_recipe_slugs: list[str], sentinel_name: str
) -> None:
    # Partial-failure probe for delete: unlike the other actions, a nonexistent
    # slug is silently skipped. The endpoint returns 200 and deletes the valid
    # recipe, so a bad slug in the batch is invisible to the caller.
    valid = two_recipe_slugs[0]
    ack = recipe_bulk_actions.delete_recipes(
        mealie_client, recipes=[valid, f"{sentinel_name}-missing"]
    )
    assert ack["deleted"] is True

    with pytest.raises(ToolError, match=r"Mealie get_recipe failed \(404"):
        recipe_crud.get_recipe(mealie_client, slug_or_id=valid)


@pytest.mark.live
def test_tag_recipes_wrapper_round_trip(
    mealie_client: AuthenticatedClient,
    two_recipe_slugs: list[str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    tag = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-tag")
    try:
        result = call_tool(
            "mealie_tag_recipes",
            {"recipes": two_recipe_slugs, "tags": [_full_object(tag)]},
        )
        assert result == {"recipes": two_recipe_slugs, "tagged": True}

        for slug in two_recipe_slugs:
            refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
            assert tag["slug"] in [t["slug"] for t in refreshed["tags"]]
    finally:
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag["id"])
