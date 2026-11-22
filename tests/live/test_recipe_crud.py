"""Live tests for the recipe CRUD lifecycle.

Each test stages a sentinel recipe (or another sentinel artifact) with the
shared fixtures, exercises a tool, asserts on the observable effect, and tears
the sentinel down even when the body fails.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import json
import os
from collections.abc import Callable, Iterator
from typing import Any
from uuid import uuid4

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
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.cook_book_create import CookBookCreate
from mealie_mcp.client.models.household_create import HouseholdCreate
from mealie_mcp.tools import (
    households_self_service,
    organizer_categories,
    organizer_tags,
    organizer_tools,
    recipe_crud,
    recipes_foods,
    recipes_units,
)
from mealie_mcp.tools._common import decode, expect_dict


def _organizer_ref(item: dict[str, str]) -> dict[str, str]:
    """A tag, category or tool reference as the recipe PATCH body expects it."""
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


@pytest.fixture
def served_image_url() -> str:
    """An image URL the Mealie instance serves itself.

    Points at the instance's own PWA icon so the image-set path resolves
    server-side without reaching any third party.
    """
    base = os.environ["MEALIE_BASE_URL"].rstrip("/")
    return f"{base}/icons/android-chrome-512x512.png"


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
    org_url = f"https://example.com/{created_recipe['name']}"
    updated = recipe_crud.update_recipe(
        mealie_client,
        slug_or_id=slug,
        description="updated by mcp-test",
        recipe_yield="6 servings",
        total_time="55 minutes",
        prep_time="15 minutes",
        perform_time="40 minutes",
        org_url=org_url,
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
    assert refreshed["orgURL"] == org_url
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
def test_update_recipe_sets_servings_and_yield_quantity(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    """Both numeric yield fields persist, and 0 clears either on its own.

    Mealie seeds both at 0, so the seeds are set to distinct non-zero values to
    tell them apart. Clearing one afterwards must leave the other standing.
    """
    slug = created_recipe["slug"]
    updated = recipe_crud.update_recipe(
        mealie_client, slug_or_id=slug, recipe_servings=6, recipe_yield_quantity=12
    )
    assert updated["recipeServings"] == 6
    assert updated["recipeYieldQuantity"] == 12

    refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert refreshed["recipeServings"] == 6
    assert refreshed["recipeYieldQuantity"] == 12

    recipe_crud.update_recipe(mealie_client, slug_or_id=slug, recipe_servings=0)
    cleared = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert cleared["recipeServings"] == 0
    assert cleared["recipeYieldQuantity"] == 12

    recipe_crud.update_recipe(mealie_client, slug_or_id=slug, recipe_yield_quantity=0)
    both_cleared = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert both_cleared["recipeYieldQuantity"] == 0


@pytest.mark.live
def test_update_recipe_time_seconds_and_text_are_independent(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    """A time text leaves the stored duration in place, and the total is never derived."""
    slug = created_recipe["slug"]
    recipe_crud.update_recipe(
        mealie_client, slug_or_id=slug, prep_time_seconds=600, perform_time_seconds=1500
    )
    stored = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert (stored["prepTimeSeconds"], stored["performTimeSeconds"]) == (600, 1500)
    assert stored["totalTimeSeconds"] is None

    prep_text = f"{sentinel_name}-prep"
    recipe_crud.update_recipe(mealie_client, slug_or_id=slug, prep_time=prep_text)
    stored = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert (stored["prepTime"], stored["prepTimeSeconds"]) == (prep_text, 600)

    recipe_crud.update_recipe(mealie_client, slug_or_id=slug, total_time_seconds=5400)
    stored = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert (stored["totalTime"], stored["totalTimeSeconds"]) == (None, 5400)


@pytest.mark.live
def test_update_recipe_step_duration_lasts_until_a_step_is_sent_without_it(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    slug = created_recipe["slug"]
    text = f"{sentinel_name}-step"
    recipe_crud.update_recipe(
        mealie_client, slug_or_id=slug, recipe_instructions=[{"text": text, "durationSeconds": 120}]
    )
    steps = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["recipeInstructions"]
    assert [(step["text"], step["durationSeconds"]) for step in steps] == [(text, 120)]

    recipe_crud.update_recipe(mealie_client, slug_or_id=slug, recipe_instructions=[{"text": text}])
    steps = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["recipeInstructions"]
    assert [(step["text"], step["durationSeconds"]) for step in steps] == [(text, None)]


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


_ORGANIZERS: dict[
    str,
    tuple[
        str,
        Callable[..., dict[str, Any]],
        Callable[..., dict[str, Any]],
        Callable[..., dict[str, Any]],
    ],
] = {
    "tags": ("tags", organizer_tags.create_tag, organizer_tags.get_tag, organizer_tags.delete_tag),
    "recipe_category": (
        "recipeCategory",
        organizer_categories.create_category,
        organizer_categories.get_category,
        organizer_categories.delete_category,
    ),
    "tools": (
        "tools",
        organizer_tools.create_tool,
        organizer_tools.get_tool,
        organizer_tools.delete_tool,
    ),
}


@pytest.mark.live
@pytest.mark.parametrize("field", list(_ORGANIZERS))
def test_update_recipe_organizer_items_resolve_against_the_catalogue(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
    field: str,
) -> None:
    """An existing id wins over the name, a known name links, a new name creates.

    The catalogue entry linked by id keeps its own name, an empty name is
    dropped, and no item rewrites the catalogue.
    """
    key, create, get, delete = _ORGANIZERS[field]
    slug = created_recipe["slug"]
    staged: list[str] = []
    minted: list[str] = []

    def stored() -> list[tuple[str, str]]:
        recipe = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        return [(item["id"], item["name"]) for item in recipe[key]]

    try:
        first = create(mealie_client, name=f"{sentinel_name}-a")
        staged.append(first["id"])
        second = create(mealie_client, name=f"{sentinel_name}-b")
        staged.append(second["id"])

        recipe_crud.update_recipe(
            mealie_client, slug_or_id=slug, **{field: [{"id": first["id"], "name": second["name"]}]}
        )
        assert stored() == [(first["id"], first["name"])]
        refetched = get(mealie_client, item_id=first["id"])
        assert (refetched["name"], refetched["slug"]) == (first["name"], first["slug"])

        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=slug,
            **{field: [{"id": str(uuid4()), "name": second["name"]}]},
        )
        assert stored() == [(second["id"], second["name"])]

        new_name = f"{sentinel_name}-new"
        recipe_crud.update_recipe(mealie_client, slug_or_id=slug, **{field: [{"name": new_name}]})
        minted = [item_id for item_id, name in stored() if name == new_name]
        assert len(minted) == 1
        assert minted[0] not in {first["id"], second["id"]}
        assert get(mealie_client, item_id=minted[0])["name"] == new_name

        recipe_crud.update_recipe(mealie_client, slug_or_id=slug, **{field: [{"name": ""}]})
        assert stored() == []
    finally:
        for item_id in [*staged, *minted]:
            with contextlib.suppress(ToolError):
                delete(mealie_client, item_id=item_id)


@pytest.mark.live
def test_update_recipe_ingredient_food_and_unit_need_id_and_name(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    """A food and a unit each need id and name together; either alone is rejected.

    The name-only arm returns a 500 because Mealie's schema offers create-by-name
    but its persistence layer looks the record up by id unconditionally. Pinning
    that status makes this fail if Mealie ever honours the arm or rejects it
    cleanly, which is when the tool docstring needs revisiting.
    """
    slug = created_recipe["slug"]
    food = recipes_foods.create_food(mealie_client, name=f"{sentinel_name}-food")
    unit = recipes_units.create_unit(mealie_client, name=f"{sentinel_name}-unit")
    unlisted_food = f"{sentinel_name}-newfood"
    unlisted_unit = f"{sentinel_name}-newunit"
    try:
        for id_only in ({"food": {"id": food["id"]}}, {"unit": {"id": unit["id"]}}):
            with pytest.raises(ToolError, match=r"Mealie update_recipe failed \(422"):
                recipe_crud.update_recipe(
                    mealie_client,
                    slug_or_id=slug,
                    recipe_ingredient=[{"note": sentinel_name, **id_only}],
                )

        for name_only in ({"food": {"name": unlisted_food}}, {"unit": {"name": unlisted_unit}}):
            with pytest.raises(ToolError, match=r"Mealie update_recipe failed \(500"):
                recipe_crud.update_recipe(
                    mealie_client,
                    slug_or_id=slug,
                    recipe_ingredient=[{"note": sentinel_name, **name_only}],
                )

        refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        assert sentinel_name not in {ing["note"] for ing in refreshed["recipeIngredient"]}

        foods = recipes_foods.list_foods(mealie_client, per_page=100)
        assert unlisted_food not in {item["name"] for item in foods["items"]}
        units = recipes_units.list_units(mealie_client, per_page=100)
        assert unlisted_unit not in {item["name"] for item in units["items"]}
    finally:
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=food["id"])
        with contextlib.suppress(ToolError):
            recipes_units.delete_unit(mealie_client, item_id=unit["id"])


@pytest.mark.live
def test_update_recipe_ingredient_reference_ids_survive_a_rewrite(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    """Rewriting the ingredient list keeps the referenceIds only when they are sent back.

    An omitted referenceId is not a no-op: Mealie mints a new one, and the step
    links still hold the old value, so they point at nothing.
    """
    slug = created_recipe["slug"]
    step_text = f"{sentinel_name}-step"
    ingredients = [{"note": f"{sentinel_name}-one"}, {"note": f"{sentinel_name}-two"}]
    recipe_crud.update_recipe(
        mealie_client,
        slug_or_id=slug,
        recipe_ingredient=ingredients,
        recipe_instructions=[{"text": step_text}],
    )
    seeded = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    ref_one, ref_two = (ing["referenceId"] for ing in seeded["recipeIngredient"])

    recipe_crud.update_recipe(
        mealie_client,
        slug_or_id=slug,
        recipe_ingredient=[
            {**ingredients[0], "referenceId": ref_one},
            {**ingredients[1], "referenceId": ref_two},
        ],
        recipe_instructions=[
            {"text": step_text, "ingredientReferences": [{"referenceId": ref_one}]}
        ],
    )
    preserved = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert [ing["referenceId"] for ing in preserved["recipeIngredient"]] == [ref_one, ref_two]
    step = preserved["recipeInstructions"][0]
    assert [link["referenceId"] for link in step["ingredientReferences"]] == [ref_one]

    recipe_crud.update_recipe(mealie_client, slug_or_id=slug, recipe_ingredient=ingredients)
    renumbered = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert {ing["referenceId"] for ing in renumbered["recipeIngredient"]}.isdisjoint(
        {ref_one, ref_two}
    )
    orphaned = renumbered["recipeInstructions"][0]
    assert [link["referenceId"] for link in orphaned["ingredientReferences"]] == [ref_one]


@pytest.mark.live
def test_update_recipe_patch_preserves_scalars_and_replaces_lists(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str], sentinel_name: str
) -> None:
    """A PATCH leaves an unsupplied field alone but replaces a supplied list wholesale."""
    slug = created_recipe["slug"]
    tag_one = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-one")
    tag_two = organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-two")
    try:
        description = f"{sentinel_name}-desc"
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=slug,
            description=description,
            tags=[
                {"id": tag_one["id"], "name": tag_one["name"], "slug": tag_one["slug"]},
                {"id": tag_two["id"], "name": tag_two["name"], "slug": tag_two["slug"]},
            ],
        )

        # A tags-only update must leave the unsupplied description untouched and
        # replace the whole tag list rather than merging, so tag two drops out.
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=slug,
            tags=[{"id": tag_one["id"], "name": tag_one["name"], "slug": tag_one["slug"]}],
        )
        refreshed = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        assert refreshed["description"] == description
        assert [t["slug"] for t in refreshed["tags"]] == [tag_one["slug"]]
    finally:
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag_one["id"])
        with contextlib.suppress(ToolError):
            organizer_tags.delete_tag(mealie_client, item_id=tag_two["id"])


@pytest.mark.live
def test_update_last_made_persists_timestamp(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    """The timestamp lands on the household's record, not on the recipe payload."""
    sent = dt.datetime(2026, 6, 1, 12, 0, 0, tzinfo=dt.UTC)
    result = recipe_crud.update_last_made(
        mealie_client, slug_or_id=created_recipe["slug"], timestamp=sent.isoformat()
    )
    assert result["slug"] == created_recipe["slug"]
    assert "lastMade" not in result
    household_recipe = households_self_service.get_household_recipe(
        mealie_client, slug_or_id=created_recipe["slug"]
    )
    returned_iso = household_recipe["lastMade"]
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
        "cookTime": "PT25M",
        "recipeIngredient": ["1 cup flour", "2 eggs"],
        "recipeInstructions": [{"@type": "HowToStep", "text": "Mix and bake."}],
    }
    result = recipe_crud.create_recipe_from_html_or_json(mealie_client, data=json.dumps(json_ld))
    slug = result["slug"]
    try:
        fetched = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        assert fetched["slug"] == slug
        # The importer stores schema.org cookTime as performTimeSeconds.
        assert fetched["performTimeSeconds"] == 25 * 60
        assert "cookTime" not in fetched
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_set_recipe_image_from_url_changes_image(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    served_image_url: str,
) -> None:
    slug = created_recipe["slug"]
    before = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert before["image"] is None

    result = recipe_crud.set_recipe_image_from_url(
        mealie_client, slug_or_id=slug, url=served_image_url
    )
    after = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert result["image"] == after["image"]
    assert after["image"] is not None

    # Each call mints a fresh key, which is what invalidates cached copies.
    again = recipe_crud.set_recipe_image_from_url(
        mealie_client, slug_or_id=slug, url=served_image_url
    )
    assert again["image"] != result["image"]
    assert recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["image"] == again["image"]


@pytest.mark.live
def test_create_recipe_asset_from_url_adds_an_asset_per_call(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    served_image_url: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """Each call adds a served image asset by slug or id and leaves the title image alone."""
    slug = created_recipe["slug"]
    recipe_id = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["id"]

    first = call_tool(
        "mealie_create_recipe_asset_from_url", {"slug_or_id": slug, "url": served_image_url}
    )
    assert first == {
        "name": "android-chrome-512x512",
        "icon": "mdi-file-image",
        "fileName": "android-chrome-512x512.png",
    }
    second = recipe_crud.create_recipe_asset_from_url(
        mealie_client, slug_or_id=recipe_id, url=served_image_url
    )
    assert second["fileName"] != first["fileName"]

    after = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert [asset["fileName"] for asset in after["assets"]] == [
        first["fileName"],
        second["fileName"],
    ]
    assert after["image"] is None

    served = mealie_client.get_httpx_client().get(
        f"/api/media/recipes/{recipe_id}/assets/{second['fileName']}"
    )
    assert served.status_code == 200
    assert served.headers["content-type"] == "image/png"


@pytest.mark.live
def test_create_recipe_asset_from_url_rejects_a_non_image_and_an_svg(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    slug = created_recipe["slug"]
    base = os.environ["MEALIE_BASE_URL"].rstrip("/")
    for url in (f"{base}/api/app/about", f"{base}/icons/safari-pinned-tab.svg"):
        with pytest.raises(ToolError, match=r"Mealie create_recipe_asset_from_url failed \(400"):
            recipe_crud.create_recipe_asset_from_url(mealie_client, slug_or_id=slug, url=url)
    assert recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["assets"] == []


@pytest.mark.live
def test_delete_recipe_image_removes_image(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    served_image_url: str,
) -> None:
    slug = created_recipe["slug"]
    recipe_crud.set_recipe_image_from_url(mealie_client, slug_or_id=slug, url=served_image_url)
    assert recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["image"] is not None

    ack = recipe_crud.delete_recipe_image(mealie_client, slug_or_id=slug)
    assert ack == {"id": slug, "deleted": True}

    after = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert after["image"] is None


@pytest.mark.live
def test_create_recipe_from_url_rejects_invalid_url(
    mealie_client: AuthenticatedClient,
) -> None:
    with pytest.raises(ToolError, match=r"Mealie create_recipe_from_url failed"):
        recipe_crud.create_recipe_from_url(mealie_client, url="https://example.com/not-a-recipe")


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
        recipe_crud.update_recipe(mealie_client, slug_or_id=with_tool, tools=[_organizer_ref(tool)])

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
def test_suggest_recipes_matches_on_food(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    food = recipes_foods.create_food(mealie_client, name=f"{sentinel_name}-food")
    with_food = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-with")["slug"]
    try:
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=with_food,
            recipe_ingredient=[
                {"note": "from mcp-test", "food": {"id": food["id"], "name": food["name"]}}
            ],
        )

        suggested = recipe_crud.suggest_recipes(mealie_client, foods=[food["id"]], limit=100)
        matched = {item["recipe"]["slug"] for item in suggested["items"]}
        assert with_food in matched

        # An unrelated, never-attached food must not surface the sentinel,
        # proving the suggestion filters rather than returning everything.
        other_food = recipes_foods.create_food(mealie_client, name=f"{sentinel_name}-other")
        try:
            unrelated = recipe_crud.suggest_recipes(
                mealie_client, foods=[other_food["id"]], limit=100
            )
            unrelated_slugs = {item["recipe"]["slug"] for item in unrelated["items"]}
            assert with_food not in unrelated_slugs
        finally:
            with contextlib.suppress(ToolError):
                recipes_foods.delete_food(mealie_client, item_id=other_food["id"])
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=with_food)
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=food["id"])


@pytest.mark.live
def test_suggest_recipes_honours_max_missing_foods(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    foods = [
        recipes_foods.create_food(mealie_client, name=f"{sentinel_name}-food-{i}") for i in range(3)
    ]
    slug = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-recipe")["slug"]
    try:
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=slug,
            recipe_ingredient=[
                {"note": food["name"], "food": {"id": food["id"], "name": food["name"]}}
                for food in foods
            ],
        )
        on_hand = [foods[0]["id"]]  # one of three foods on hand, so two are missing

        # A generous budget keeps the recipe: two missing foods is within five.
        loose = recipe_crud.suggest_recipes(
            mealie_client, foods=on_hand, max_missing_foods=5, limit=100
        )
        assert any(item["recipe"]["slug"] == slug for item in loose["items"])

        # Tightening the budget below the two missing foods drops the recipe.
        tight = recipe_crud.suggest_recipes(
            mealie_client, foods=on_hand, max_missing_foods=1, limit=100
        )
        assert all(item["recipe"]["slug"] != slug for item in tight["items"])
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        for food in foods:
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
        with contextlib.suppress(ToolError):
            expect_dict(
                "delete_household",
                delete_one_api_admin_households_item_id_delete.sync_detailed(
                    other["id"], client=mealie_client
                ),
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
                body=CookBookCreate(name=f"{sentinel_name}-cb", query_filter_string=query),
            ).content
        )

        matched = _result_slugs(
            recipe_crud.list_recipes(mealie_client, cookbook=cookbook["slug"], per_page=100)
        )
        assert in_book in matched
        assert out_book not in matched
    finally:
        if cookbook is not None:
            with contextlib.suppress(ToolError):
                expect_dict(
                    "delete_cookbook",
                    delete_one_api_households_cookbooks_item_id_delete.sync_detailed(
                        cookbook["id"], client=mealie_client
                    ),
                )
        for slug in (in_book, out_book):
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        with contextlib.suppress(ToolError):
            organizer_categories.delete_category(mealie_client, item_id=category["id"])
