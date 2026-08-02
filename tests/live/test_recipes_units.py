"""Live tests for the unit lifecycle and the unit merge.

Stages a sentinel unit, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipes_units import update_one_api_units_item_id_put
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_unit import CreateIngredientUnit
from mealie_mcp.tools import (
    households_shopping_list_items,
    households_shopping_lists,
    recipe_crud,
    recipes_units,
)
from mealie_mcp.tools._common import expect_dict

SEED_STANDARD_QUANTITY = 2.5


def _list_item(client: AuthenticatedClient, list_id: str, item_id: str) -> dict[str, Any]:
    """Read one item back off its shopping list."""
    items = households_shopping_lists.get_shopping_list(client, list_id=list_id)["listItems"]
    found = next((entry for entry in items if entry["id"] == item_id), None)
    assert found is not None, f"shopping list item {item_id} is not on list {list_id}"
    return dict(found)


@pytest.fixture
def created_unit(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Stage a sentinel unit via `create_unit`, then seed unexposed fields.

    Staging through the tool gives `create_unit` live coverage for the
    descriptive fields, with both booleans set to their non-default values.
    `standard_quantity` and `standard_unit` are body-model fields the unit
    tools do not expose, so they are the ones a naive PUT would silently
    clobber. They are seeded with a direct PUT built from the created payload,
    so an update that touches only exposed fields must leave them intact.
    `extras` is not used as a seed because Mealie accepts it on the unit PUT
    but does not persist it, and `standard_quantity` only persists when the
    same body carries a non-null `standard_unit`.
    """
    created = recipes_units.create_unit(
        mealie_client,
        name=sentinel_name,
        abbreviation=f"{sentinel_name}-abbr",
        plural_name=f"{sentinel_name}-plural",
        plural_abbreviation=f"{sentinel_name}-plural-abbr",
        description=f"{sentinel_name}-description",
        use_abbreviation=True,
        fraction=False,
        aliases=[f"{sentinel_name}-alias-1", f"{sentinel_name}-alias-2"],
    )
    item_id = str(created["id"])
    try:
        assert created["name"] == sentinel_name
        assert created["abbreviation"] == f"{sentinel_name}-abbr"
        assert created["pluralName"] == f"{sentinel_name}-plural"
        assert created["pluralAbbreviation"] == f"{sentinel_name}-plural-abbr"
        assert created["description"] == f"{sentinel_name}-description"
        assert created["useAbbreviation"] is True
        assert created["fraction"] is False
        assert {alias["name"] for alias in created["aliases"]} == {
            f"{sentinel_name}-alias-1",
            f"{sentinel_name}-alias-2",
        }

        seed = CreateIngredientUnit.from_dict(created)
        seed.additional_properties = {}
        seed.standard_quantity = SEED_STANDARD_QUANTITY
        seed.standard_unit = f"{sentinel_name}-std-unit"
        expect_dict(
            "seed_unit_fields",
            update_one_api_units_item_id_put.sync_detailed(
                item_id, client=mealie_client, body=seed
            ),
        )

        yield {"id": item_id, "name": sentinel_name}
    finally:
        with contextlib.suppress(ToolError):
            recipes_units.delete_unit(mealie_client, item_id=item_id)


@pytest.mark.live
def test_unit_lifecycle(mealie_client: AuthenticatedClient, created_unit: dict[str, str]) -> None:
    item_id = created_unit["id"]
    name = created_unit["name"]

    seeded_aliases = {f"{name}-alias-1", f"{name}-alias-2"}

    fetched = recipes_units.get_unit(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == name
    assert fetched["abbreviation"] == f"{name}-abbr"
    assert fetched["pluralName"] == f"{name}-plural"
    assert fetched["pluralAbbreviation"] == f"{name}-plural-abbr"
    assert fetched["useAbbreviation"] is True
    assert fetched["fraction"] is False
    assert {alias["name"] for alias in fetched["aliases"]} == seeded_aliases
    assert fetched["description"] == f"{name}-description"
    assert fetched["standardQuantity"] == SEED_STANDARD_QUANTITY
    assert fetched["standardUnit"] == f"{name}-std-unit"

    listing = recipes_units.list_units(mealie_client, search=name, per_page=100)
    assert any(u["id"] == item_id for u in listing["items"])

    renamed = f"{name}-renamed"
    updated = recipes_units.update_unit(mealie_client, item_id=item_id, name=renamed)
    assert updated["id"] == item_id
    assert updated["name"] == renamed
    assert updated["abbreviation"] == f"{name}-abbr"
    assert updated["pluralName"] == f"{name}-plural"
    assert updated["pluralAbbreviation"] == f"{name}-plural-abbr"
    assert updated["useAbbreviation"] is True
    assert updated["fraction"] is False
    assert {alias["name"] for alias in updated["aliases"]} == seeded_aliases
    assert updated["description"] == f"{name}-description"
    assert updated["standardQuantity"] == SEED_STANDARD_QUANTITY
    assert updated["standardUnit"] == f"{name}-std-unit"

    updated = recipes_units.update_unit(
        mealie_client,
        item_id=item_id,
        abbreviation=f"{name}-abbr-2",
        description=f"{name}-description-2",
        use_abbreviation=False,
        aliases=[f"{name}-alias-3"],
    )
    assert updated["name"] == renamed
    assert updated["abbreviation"] == f"{name}-abbr-2"
    assert updated["description"] == f"{name}-description-2"
    assert updated["useAbbreviation"] is False
    assert {alias["name"] for alias in updated["aliases"]} == {f"{name}-alias-3"}
    assert updated["pluralName"] == f"{name}-plural"
    assert updated["pluralAbbreviation"] == f"{name}-plural-abbr"
    assert updated["fraction"] is False
    assert updated["standardQuantity"] == SEED_STANDARD_QUANTITY
    assert updated["standardUnit"] == f"{name}-std-unit"

    refetched = recipes_units.get_unit(mealie_client, item_id=item_id)
    assert refetched["abbreviation"] == f"{name}-abbr-2"
    assert refetched["description"] == f"{name}-description-2"
    assert refetched["useAbbreviation"] is False
    assert {alias["name"] for alias in refetched["aliases"]} == {f"{name}-alias-3"}

    ack = recipes_units.delete_unit(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_unit failed \(404"):
        recipes_units.get_unit(mealie_client, item_id=item_id)


@pytest.mark.live
def test_update_unit_empty_values_clear_text_and_aliases(
    mealie_client: AuthenticatedClient, created_unit: dict[str, str]
) -> None:
    item_id = created_unit["id"]
    # An empty string clears the abbreviation, plural name, plural
    # abbreviation, and description, and an empty list clears the aliases,
    # rather than being skipped the way an omitted (None) field is.
    updated = recipes_units.update_unit(
        mealie_client,
        item_id=item_id,
        abbreviation="",
        plural_name="",
        plural_abbreviation="",
        description="",
        aliases=[],
    )
    assert updated["abbreviation"] == ""
    assert updated["pluralName"] == ""
    assert updated["pluralAbbreviation"] == ""
    assert updated["description"] == ""
    assert updated["aliases"] == []
    refetched = recipes_units.get_unit(mealie_client, item_id=item_id)
    assert refetched["abbreviation"] == ""
    assert refetched["pluralName"] == ""
    assert refetched["pluralAbbreviation"] == ""
    assert refetched["description"] == ""
    assert refetched["aliases"] == []


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_create_unit_round_trips_fields_through_wrapper(
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """The wrapper forwards the descriptive fields, booleans, and aliases."""
    created = call_tool(
        "mealie_create_unit",
        {
            "name": sentinel_name,
            "abbreviation": f"{sentinel_name}-abbr",
            "plural_name": f"{sentinel_name}-plural",
            "plural_abbreviation": f"{sentinel_name}-plural-abbr",
            "description": f"{sentinel_name}-description",
            "use_abbreviation": True,
            "fraction": False,
            "aliases": [f"{sentinel_name}-alias"],
        },
    )
    assert isinstance(created, dict)
    item_id = str(created["id"])
    try:
        assert created["name"] == sentinel_name
        assert created["abbreviation"] == f"{sentinel_name}-abbr"
        assert created["pluralName"] == f"{sentinel_name}-plural"
        assert created["pluralAbbreviation"] == f"{sentinel_name}-plural-abbr"
        assert created["description"] == f"{sentinel_name}-description"
        assert created["useAbbreviation"] is True
        assert created["fraction"] is False
        assert [alias["name"] for alias in created["aliases"]] == [f"{sentinel_name}-alias"]
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_unit", {"item_id": item_id})


@pytest.mark.live
def test_create_unit_name_only_leaves_defaults(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    """A name-only create sends no optional fields, so Mealie's defaults apply."""
    created = recipes_units.create_unit(mealie_client, name=sentinel_name)
    item_id = str(created["id"])
    try:
        fetched = recipes_units.get_unit(mealie_client, item_id=item_id)
        assert fetched["abbreviation"] == ""
        assert fetched["description"] == ""
        assert fetched["useAbbreviation"] is False
        assert fetched["fraction"] is True
        assert fetched["aliases"] == []
    finally:
        with contextlib.suppress(ToolError):
            recipes_units.delete_unit(mealie_client, item_id=item_id)


@pytest.mark.live
def test_merge_unit_moves_ingredients_and_deletes_the_source(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """The merge repoints recipe ingredients and drops the source and its aliases.

    The shopping list item is read before and after, so the claim that it keeps
    the deleted id and resolves to no unit is observed as a change rather than
    an absence. The merge runs through the wrapper because both arguments are
    ids of the same type, where a swapped forward would delete the surviving
    unit.
    """
    source = recipes_units.create_unit(
        mealie_client, name=f"{sentinel_name}-source", aliases=[f"{sentinel_name}-source-alias"]
    )
    target = recipes_units.create_unit(
        mealie_client, name=f"{sentinel_name}-target", aliases=[f"{sentinel_name}-target-alias"]
    )
    source_id, target_id = str(source["id"]), str(target["id"])
    slug: str | None = None
    list_id: str | None = None
    item_id: str | None = None
    try:
        recipe = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-recipe")
        slug = recipe["slug"]
        shopping_list = households_shopping_lists.create_shopping_list(
            mealie_client, name=f"{sentinel_name}-list"
        )
        list_id = str(shopping_list["id"])
        item = households_shopping_list_items.add_shopping_list_item(
            mealie_client,
            shopping_list_id=list_id,
            note=f"{sentinel_name}-item",
            unit_id=source_id,
        )
        item_id = str(item["id"])
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=slug,
            recipe_ingredient=[
                {
                    "note": f"{sentinel_name}-ingredient",
                    "unit": {"id": source_id, "name": source["name"]},
                }
            ],
        )
        staged = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        assert staged["recipeIngredient"][0]["unit"]["id"] == source_id
        linked = _list_item(mealie_client, list_id, item_id)
        assert linked["unitId"] == source_id
        assert linked["unit"]["id"] == source_id

        ack = call_tool("mealie_merge_unit", {"from_unit_id": source_id, "to_unit_id": target_id})
        assert ack == {"from_unit_id": source_id, "to_unit_id": target_id, "merged": True}

        merged = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        assert merged["recipeIngredient"][0]["unit"]["id"] == target_id
        with pytest.raises(ToolError, match=r"Mealie get_unit failed \(404"):
            recipes_units.get_unit(mealie_client, item_id=source_id)

        survivor = recipes_units.get_unit(mealie_client, item_id=target_id)
        assert [alias["name"] for alias in survivor["aliases"]] == [f"{sentinel_name}-target-alias"]

        stranded = _list_item(mealie_client, list_id, item_id)
        assert stranded["unitId"] == source_id
        assert stranded["unit"] is None
    finally:
        if item_id is not None:
            with contextlib.suppress(ToolError):
                households_shopping_list_items.delete_shopping_list_item(
                    mealie_client, item_id=item_id
                )
        if list_id is not None:
            with contextlib.suppress(ToolError):
                households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)
        if slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        for unit_id in (source_id, target_id):
            with contextlib.suppress(ToolError):
                recipes_units.delete_unit(mealie_client, item_id=unit_id)
