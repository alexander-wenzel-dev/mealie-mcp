"""Live tests for the tool (equipment) lifecycle, the empty list, and the merge.

Stages sentinel tools, recipes, a cookbook, and a meal plan rule, exercises
the read, list, update, delete, and merge tools, and tears the sentinels
down even when the body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_self_service import (
    get_logged_in_user_household_api_households_self_get,
)
from mealie_mcp.client.api.organizer_tools import update_one_api_organizers_tools_item_id_put
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.tool_create import ToolCreate
from mealie_mcp.tools import (
    households_cookbooks,
    households_meal_plan_rules,
    organizer_tools,
    recipe_crud,
)
from mealie_mcp.tools._common import expect_dict


def _ref(organizer: dict[str, Any]) -> dict[str, Any]:
    """Reduce an organizer payload to the reference a recipe update accepts."""
    return {"id": organizer["id"], "name": organizer["name"], "slug": organizer["slug"]}


@pytest.fixture
def created_tool(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, object]]:
    """Stage a sentinel tool via `create_tool`, then seed `households_with_tool`.

    Staging through the tool gives `create_tool` live coverage. `households_with_tool`
    is the only field on the create body model that `update_tool` does not expose,
    so it is the one a naive PUT would silently overwrite. It is seeded with a
    direct PUT carrying the current user's household id so the lifecycle test can
    verify that `update_tool` preserves the untouched field when only `name`
    is changed. Mealie's PUT silently drops household ids passed for this field
    and stores only the slug, so the seed uses the current user's household
    slug to round-trip cleanly through the GET-then-PUT merge.
    """
    self_household = expect_dict(
        "households_self",
        get_logged_in_user_household_api_households_self_get.sync_detailed(client=mealie_client),
    )
    households_seed = [str(self_household["slug"])]

    created = organizer_tools.create_tool(mealie_client, name=sentinel_name)
    item_id = created["id"]
    assert created["name"] == sentinel_name

    try:
        expect_dict(
            "seed_tool_households",
            update_one_api_organizers_tools_item_id_put.sync_detailed(
                item_id,
                client=mealie_client,
                body=ToolCreate(name=sentinel_name, households_with_tool=households_seed),
            ),
        )
        yield {
            "id": item_id,
            "name": sentinel_name,
            "households_with_tool": households_seed,
        }
    finally:
        with contextlib.suppress(ToolError):
            organizer_tools.delete_tool(mealie_client, item_id=item_id)


@pytest.mark.live
def test_tool_lifecycle(
    mealie_client: AuthenticatedClient, created_tool: dict[str, object]
) -> None:
    item_id = str(created_tool["id"])
    households_seed = created_tool["households_with_tool"]

    fetched = organizer_tools.get_tool(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == created_tool["name"]
    assert fetched["householdsWithTool"] == households_seed

    listing = organizer_tools.list_tools(
        mealie_client, search=str(created_tool["name"]), per_page=100
    )
    assert any(t["id"] == item_id for t in listing["items"])

    matched = next(t for t in listing["items"] if t["id"] == item_id)
    by_slug = organizer_tools.get_tool_by_slug(mealie_client, slug=matched["slug"])
    assert by_slug["id"] == item_id

    updated_name = f"{created_tool['name']}-renamed"
    updated = organizer_tools.update_tool(mealie_client, item_id=item_id, name=updated_name)
    assert updated["id"] == item_id
    assert updated["name"] == updated_name
    assert updated["householdsWithTool"] == households_seed

    ack = organizer_tools.delete_tool(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_tool failed \(404"):
        organizer_tools.get_tool(mealie_client, item_id=item_id)


@pytest.mark.live
def test_get_tool_by_id_omits_recipes_while_by_slug_hydrates(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    tool = organizer_tools.create_tool(mealie_client, name=sentinel_name)
    tool_id = tool["id"]
    recipe_slug: str | None = None
    try:
        recipe_slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=recipe_slug,
            tools=[{"id": tool_id, "name": tool["name"], "slug": tool["slug"]}],
        )

        # The by-id read returns a compact payload with no recipes list.
        by_id = organizer_tools.get_tool(mealie_client, item_id=tool_id)
        assert "recipes" not in by_id

        # The by-slug read hydrates recipes, including the one just attached.
        by_slug = organizer_tools.get_tool_by_slug(mealie_client, slug=tool["slug"])
        assert any(r["slug"] == recipe_slug for r in by_slug["recipes"])
    finally:
        if recipe_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe_slug)
        with contextlib.suppress(ToolError):
            organizer_tools.delete_tool(mealie_client, item_id=tool_id)


@pytest.mark.live
def test_empty_tools_drops_a_tool_once_a_recipe_uses_it(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    tool_id: str | None = None
    recipe_slug: str | None = None
    try:
        tool = organizer_tools.create_tool(mealie_client, name=sentinel_name)
        tool_id = str(tool["id"])
        empty = organizer_tools.list_empty_tools(mealie_client)
        listed = next((t for t in empty if t["id"] == tool_id), None)
        assert listed is not None, f"unused tool {tool_id} missing from the empty list"
        assert listed["recipeCount"] == 0

        recipe_slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_crud.update_recipe(mealie_client, slug_or_id=recipe_slug, tools=[_ref(tool)])

        assert all(t["id"] != tool_id for t in organizer_tools.list_empty_tools(mealie_client))
    finally:
        if recipe_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe_slug)
        if tool_id is not None:
            with contextlib.suppress(ToolError):
                organizer_tools.delete_tool(mealie_client, item_id=tool_id)


@pytest.mark.live
def test_merge_tool_repoints_recipes_and_deletes_the_source(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """The merge moves recipes to the target, once each, and drops the source.

    The source's on-hand households do not reach the target. The merge runs
    through the wrapper because both arguments are ids of the same type, where
    a swapped forward would delete the surviving tool.
    """
    tool_ids: list[str] = []
    slugs: list[str] = []
    cookbook_id: str | None = None
    rule_id: str | None = None
    try:
        source = organizer_tools.create_tool(mealie_client, name=f"{sentinel_name}-source")
        tool_ids.append(str(source["id"]))
        target = organizer_tools.create_tool(mealie_client, name=f"{sentinel_name}-target")
        tool_ids.append(str(target["id"]))
        source_id, target_id = tool_ids
        source_filter = f'tools.id IN ["{source_id}"]'
        self_household = expect_dict(
            "households_self",
            get_logged_in_user_household_api_households_self_get.sync_detailed(
                client=mealie_client
            ),
        )
        expect_dict(
            "seed_tool_households",
            update_one_api_organizers_tools_item_id_put.sync_detailed(
                source_id,
                client=mealie_client,
                body=ToolCreate(
                    name=source["name"], households_with_tool=[str(self_household["slug"])]
                ),
            ),
        )
        seeded = organizer_tools.get_tool(mealie_client, item_id=source_id)
        assert seeded["householdsWithTool"] == [self_household["slug"]]

        only_source = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-only")
        slugs.append(only_source["slug"])
        both = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-both")
        slugs.append(both["slug"])
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=only_source["slug"], tools=[_ref(source)]
        )
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=both["slug"], tools=[_ref(source), _ref(target)]
        )
        cookbook_id = households_cookbooks.create_cookbook(
            mealie_client, name=f"{sentinel_name}-cookbook", query_filter_string=source_filter
        )["id"]
        rule_id = households_meal_plan_rules.create_mealplan_rule(
            mealie_client, query_filter_string=source_filter
        )["id"]

        survivor = call_tool(
            "mealie_merge_tool", {"from_tool_id": source_id, "to_tool_id": target_id}
        )
        assert isinstance(survivor, dict)
        assert survivor["id"] == target_id
        assert survivor["householdsWithTool"] == []

        for slug in slugs:
            carried = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["tools"]
            assert [entry["id"] for entry in carried] == [target_id]
        with pytest.raises(ToolError, match=r"Mealie get_tool failed \(404"):
            organizer_tools.get_tool(mealie_client, item_id=source_id)

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
        for item_id in tool_ids:
            with contextlib.suppress(ToolError):
                organizer_tools.delete_tool(mealie_client, item_id=item_id)
