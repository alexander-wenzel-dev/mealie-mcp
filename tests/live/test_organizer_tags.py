"""Live tests for the tag lifecycle and the tag merge.

Stages sentinel tags, recipes, a cookbook, and a meal plan rule, exercises
the read, list, update, delete, and merge tools, and tears the sentinels
down even when the body fails so no `mcp-test-` data lingers.
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
    organizer_tags,
    recipe_crud,
)


def _ref(organizer: dict[str, Any]) -> dict[str, Any]:
    """Reduce an organizer payload to the reference a recipe update accepts."""
    return {"id": organizer["id"], "name": organizer["name"], "slug": organizer["slug"]}


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
def test_create_tag_rejects_a_duplicate_name(
    mealie_client: AuthenticatedClient, created_tag: dict[str, str]
) -> None:
    with pytest.raises(ToolError) as excinfo:
        organizer_tags.create_tag(mealie_client, name=created_tag["name"])

    message = str(excinfo.value)
    assert message.startswith("Mealie create_tag failed (409): ")

    # Mealie attaches its raw database error to a conflict, so this is also the
    # call where that text would reach a tool caller.
    reported = message.split("): ", 1)[1]
    assert reported
    for fragment in ("[SQL:", "[parameters:", "IntegrityError", '"exception"'):
        assert fragment not in reported, f"{fragment} reached the caller: {reported}"


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


@pytest.mark.live
def test_get_tag_by_id_leaves_recipes_empty_while_by_slug_hydrates(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    tag = organizer_tags.create_tag(mealie_client, name=sentinel_name)
    tag_id = tag["id"]
    recipe_slug: str | None = None
    try:
        recipe_slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=recipe_slug,
            tags=[{"id": tag_id, "name": tag["name"], "slug": tag["slug"]}],
        )

        # The by-id read carries a recipes key but never populates it, even
        # though the tag is now in use.
        by_id = organizer_tags.get_tag(mealie_client, item_id=tag_id)
        assert by_id["recipes"] == []

        # The by-slug read hydrates recipes, including the one just attached.
        by_slug = organizer_tags.get_tag_by_slug(mealie_client, slug=tag["slug"])
        assert any(r["slug"] == recipe_slug for r in by_slug["recipes"])
    finally:
        if recipe_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe_slug)
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag_id)


@pytest.mark.live
def test_merge_tag_repoints_recipes_and_deletes_the_source(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """The merge moves recipes to the target, once each, and drops the source.

    The merge runs through the wrapper because both arguments are ids of the
    same type, where a swapped forward would delete the surviving tag.
    """
    source = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-source")
    target = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-target")
    source_id, target_id = str(source["id"]), str(target["id"])
    source_filter = f'tags.id IN ["{source_id}"]'
    slugs: list[str] = []
    cookbook_id: str | None = None
    rule_id: str | None = None
    try:
        only_source = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-only")
        slugs.append(only_source["slug"])
        both = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-both")
        slugs.append(both["slug"])
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=only_source["slug"], tags=[_ref(source)]
        )
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=both["slug"], tags=[_ref(source), _ref(target)]
        )
        cookbook_id = households_cookbooks.create_cookbook(
            mealie_client, name=f"{sentinel_name}-cookbook", query_filter_string=source_filter
        )["id"]
        rule_id = households_meal_plan_rules.create_mealplan_rule(
            mealie_client, query_filter_string=source_filter
        )["id"]

        survivor = call_tool("mealie_merge_tag", {"from_tag_id": source_id, "to_tag_id": target_id})
        assert isinstance(survivor, dict)
        assert survivor["id"] == target_id

        for slug in slugs:
            carried = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["tags"]
            assert [entry["id"] for entry in carried] == [target_id]
        with pytest.raises(ToolError, match=r"Mealie get_tag failed \(404"):
            organizer_tags.get_tag(mealie_client, item_id=source_id)

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
                organizer_tags.delete_tag(mealie_client, item_id=item_id)
