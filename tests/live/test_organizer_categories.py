"""Live tests for the category lifecycle and the category merge.

Stages sentinel categories, recipes, a cookbook, and a meal plan rule,
exercises the read, list, update, delete, and merge tools, and tears the
sentinels down even when the body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import (
    households_cookbooks,
    households_meal_plan_rules,
    organizer_categories,
    recipe_crud,
)


def _ref(organizer: dict[str, Any]) -> dict[str, Any]:
    """Reduce an organizer payload to the reference a recipe update accepts."""
    return {"id": organizer["id"], "name": organizer["name"], "slug": organizer["slug"]}


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


@pytest.mark.live
def test_merge_category_repoints_recipes_and_deletes_the_source(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """The merge moves recipes to the target, once each, and drops the source.

    The merge runs through the wrapper because both arguments are ids of the
    same type, where a swapped forward would delete the surviving category.
    """
    source = organizer_categories.create_category(mealie_client, name=f"{sentinel_name}-source")
    target = organizer_categories.create_category(mealie_client, name=f"{sentinel_name}-target")
    source_id, target_id = str(source["id"]), str(target["id"])
    source_filter = f'recipe_category.id IN ["{source_id}"]'
    slugs: list[str] = []
    cookbook_id: str | None = None
    rule_id: str | None = None
    try:
        only_source = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-only")
        slugs.append(only_source["slug"])
        both = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-both")
        slugs.append(both["slug"])
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=only_source["slug"], recipe_category=[_ref(source)]
        )
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=both["slug"], recipe_category=[_ref(source), _ref(target)]
        )
        cookbook_id = households_cookbooks.create_cookbook(
            mealie_client, name=f"{sentinel_name}-cookbook", query_filter_string=source_filter
        )["id"]
        rule_id = households_meal_plan_rules.create_mealplan_rule(
            mealie_client, query_filter_string=source_filter
        )["id"]

        survivor = call_tool(
            "mealie_merge_category", {"from_category_id": source_id, "to_category_id": target_id}
        )
        assert isinstance(survivor, dict)
        assert survivor["id"] == target_id

        for slug in slugs:
            carried = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["recipeCategory"]
            assert [entry["id"] for entry in carried] == [target_id]
        with pytest.raises(ToolError, match=r"Mealie get_category failed \(404"):
            organizer_categories.get_category(mealie_client, item_id=source_id)

        cookbook = households_cookbooks.get_cookbook(mealie_client, item_id=cookbook_id)
        assert cookbook["queryFilterString"] == source_filter
        rule = households_meal_plan_rules.get_mealplan_rule(mealie_client, item_id=rule_id)
        assert rule["queryFilterString"] == source_filter
    finally:
        if rule_id is not None:
            with contextlib.suppress(ToolError):
                households_meal_plan_rules.delete_mealplan_rule(mealie_client, item_id=rule_id)
        if cookbook_id is not None:
            with contextlib.suppress(ToolError):
                households_cookbooks.delete_cookbook(mealie_client, item_id=cookbook_id)
        for slug in slugs:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        for item_id in (source_id, target_id):
            with contextlib.suppress(ToolError):
                organizer_categories.delete_category(mealie_client, item_id=item_id)
