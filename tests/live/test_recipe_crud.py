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

from mealie_mcp.client.api.admin_manage_groups import get_all_api_admin_groups_get
from mealie_mcp.client.api.admin_manage_households import (
    create_one_api_admin_households_post,
    delete_one_api_admin_households_item_id_delete,
    get_all_api_admin_households_get,
)
from mealie_mcp.client.api.households_cookbooks import (
    create_one_api_households_cookbooks_post,
    delete_one_api_households_cookbooks_item_id_delete,
)
from mealie_mcp.client.api.recipe_crud import patch_one_api_recipes_slug_patch
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_cook_book import CreateCookBook
from mealie_mcp.client.models.household_create import HouseholdCreate
from mealie_mcp.client.models.recipe import Recipe
from mealie_mcp.tools import (
    organizer_categories,
    organizer_tags,
    organizer_tools,
    recipe_crud,
    recipes_foods,
)
from mealie_mcp.tools._common import decode


def _organizer_ref(item: dict[str, str]) -> dict[str, str]:
    """A tag or category reference as the recipe PATCH body expects it."""
    return {"id": item["id"], "name": item["name"], "slug": item["slug"]}


def _result_slugs(listing: dict[str, object]) -> set[str]:
    items = listing["items"]
    assert isinstance(items, list)
    return {item["slug"] for item in items}


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


@pytest.mark.live
def test_list_recipes_filters_by_tags_and_require_all(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    # require_all_* is symmetric across categories/tags/tools/foods, so tags
    # alone exercises the any-vs-all behaviour for the whole family.
    tag_a = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-a")
    tag_b = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-b")
    both = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-both")["slug"]
    one = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-one")["slug"]
    try:
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=both, tags=[_organizer_ref(tag_a), _organizer_ref(tag_b)]
        )
        recipe_crud.update_recipe(mealie_client, slug_or_id=one, tags=[_organizer_ref(tag_a)])

        match_any = _result_slugs(
            recipe_crud.list_recipes(
                mealie_client, tags=[tag_a["slug"], tag_b["slug"]], per_page=100
            )
        )
        assert both in match_any
        assert one in match_any

        match_all = _result_slugs(
            recipe_crud.list_recipes(
                mealie_client,
                tags=[tag_a["slug"], tag_b["slug"]],
                require_all_tags=True,
                per_page=100,
            )
        )
        assert both in match_all
        assert one not in match_all
    finally:
        for slug in (both, one):
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        for tag in (tag_a, tag_b):
            with contextlib.suppress(ToolError):
                organizer_tags.delete_tag(mealie_client, item_id=tag["id"])


@pytest.mark.live
def test_list_recipes_filters_by_tools(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    tool = organizer_tools.create_tool(mealie_client, name=f"{sentinel_name}-tool")
    with_tool = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-with")["slug"]
    without_tool = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-without")["slug"]
    try:
        # No tool exposes recipe-equipment linkage, so attach via the raw PATCH.
        patch_body = Recipe.from_dict(
            {"tools": [{"id": tool["id"], "name": tool["name"], "slug": tool["slug"]}]}
        )
        patch_one_api_recipes_slug_patch.sync_detailed(
            with_tool, client=mealie_client, body=patch_body
        )

        matched = _result_slugs(
            recipe_crud.list_recipes(mealie_client, tools=[tool["slug"]], per_page=100)
        )
        assert with_tool in matched
        assert without_tool not in matched
    finally:
        for slug in (with_tool, without_tool):
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        with contextlib.suppress(ToolError):
            organizer_tools.delete_tool(mealie_client, item_id=tool["id"])


@pytest.mark.live
def test_list_recipes_filters_by_foods(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    food = recipes_foods.create_food(mealie_client, name=f"{sentinel_name}-food")
    with_food = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-with")["slug"]
    without_food = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-without")["slug"]
    try:
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=with_food,
            recipe_ingredient=[
                {"note": "from mcp-test", "food": {"id": food["id"], "name": food["name"]}}
            ],
        )

        # Foods carry no slug, so the filter takes the food id.
        matched = _result_slugs(
            recipe_crud.list_recipes(mealie_client, foods=[food["id"]], per_page=100)
        )
        assert with_food in matched
        assert without_food not in matched
    finally:
        for slug in (with_food, without_food):
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=food["id"])


@pytest.mark.live
def test_list_recipes_filters_by_households(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    # The sentinel recipe lives in the token's own household. A freshly created
    # empty household gives a clean absence: the recipe is in its own household
    # but not in the other one. No tool wraps household admin, so use the client.
    recipe = recipe_crud.get_recipe(mealie_client, slug_or_id=created_recipe["slug"])
    own_household_id = recipe["householdId"]
    households = decode(
        get_all_api_admin_households_get.sync_detailed(client=mealie_client).content
    )
    own_slug = next(h["slug"] for h in households["items"] if h["id"] == own_household_id)
    group_id = decode(get_all_api_admin_groups_get.sync_detailed(client=mealie_client).content)[
        "items"
    ][0]["id"]
    other = decode(
        create_one_api_admin_households_post.sync_detailed(
            client=mealie_client,
            body=HouseholdCreate(name=f"{sentinel_name}-hh", group_id=group_id),
        ).content
    )
    try:
        in_own = _result_slugs(
            recipe_crud.list_recipes(
                mealie_client,
                households=[own_slug],
                search=created_recipe["name"],
                per_page=100,
            )
        )
        assert created_recipe["slug"] in in_own

        in_other = _result_slugs(
            recipe_crud.list_recipes(
                mealie_client,
                households=[other["slug"]],
                search=created_recipe["name"],
                per_page=100,
            )
        )
        assert created_recipe["slug"] not in in_other
    finally:
        delete_one_api_admin_households_item_id_delete.sync_detailed(
            other["id"], client=mealie_client
        )


@pytest.mark.live
def test_list_recipes_filters_by_cookbook(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    category = organizer_categories.create_category(mealie_client, name=f"{sentinel_name}-cat")
    in_book = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-in")["slug"]
    out_book = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-out")["slug"]
    cookbook: dict[str, str] | None = None
    try:
        recipe_crud.update_recipe(
            mealie_client, slug_or_id=in_book, recipe_category=[_organizer_ref(category)]
        )
        # A cookbook filters by its saved query string; match the sentinel category.
        query = f'recipe_category.id CONTAINS ALL ["{category["id"]}"]'
        cookbook = decode(
            create_one_api_households_cookbooks_post.sync_detailed(
                client=mealie_client,
                body=CreateCookBook(name=f"{sentinel_name}-cb", query_filter_string=query),
            ).content
        )

        matched = _result_slugs(
            recipe_crud.list_recipes(mealie_client, cookbook=cookbook["slug"], per_page=100)
        )
        assert in_book in matched
        assert out_book not in matched
    finally:
        if cookbook is not None:
            with contextlib.suppress(Exception):
                delete_one_api_households_cookbooks_item_id_delete.sync_detailed(
                    cookbook["id"], client=mealie_client
                )
        for slug in (in_book, out_book):
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        with contextlib.suppress(ToolError):
            organizer_categories.delete_category(mealie_client, item_id=category["id"])
