"""Live tests for the household shopping list item tools.

Stages a sentinel shopping list, adds sentinel items, and exercises the single
and bulk write tools against it. The partial updates change one field at a time
and assert that the unsupplied fields and the item's food and unit links
survive the PUT-replace, so a regression in fetch-then-merge fails the test.
Food, unit, and label sentinels back the aggregation and labelling assertions.
Every test signature requests the list fixture last so pytest tears the list
(and cascades its items) down before the label, unit, and food, and cleanup
runs even when the body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.groups_multi_purpose_labels import (
    create_one_api_groups_labels_post,
    delete_one_api_groups_labels_item_id_delete,
)
from mealie_mcp.client.api.households_shopping_list_items import (
    get_one_api_households_shopping_items_item_id_get,
    update_one_api_households_shopping_items_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.multi_purpose_label_create import MultiPurposeLabelCreate
from mealie_mcp.client.models.shopping_list_item_update import ShoppingListItemUpdate
from mealie_mcp.tools import (
    households_shopping_list_items,
    households_shopping_lists,
    recipe_crud,
    recipes_foods,
    recipes_units,
)
from mealie_mcp.tools._common import expect_dict

# Names no list and no item. Mealie validates the id as a version 4 UUID and
# answers a 422 for any other shape, before it looks the id up.
ABSENT_UUID = "8f14e45f-ceea-4a67-b98d-4f5e2f2a1b3c"


@pytest.fixture
def created_shopping_list(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel shopping list to hold the items and tear it down."""
    created = households_shopping_lists.create_shopping_list(mealie_client, name=sentinel_name)
    list_id = created["id"]
    try:
        yield {"id": list_id}
    finally:
        with contextlib.suppress(ToolError):
            households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)


@pytest.fixture
def created_food(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel food to bind onto the item and tear it down."""
    food = recipes_foods.create_food(mealie_client, name=f"{sentinel_name}-food")
    try:
        yield {"id": food["id"]}
    finally:
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=food["id"])


@pytest.fixture
def created_unit(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel unit to bind onto the item and tear it down."""
    unit = recipes_units.create_unit(mealie_client, name=f"{sentinel_name}-unit")
    try:
        yield {"id": unit["id"]}
    finally:
        with contextlib.suppress(ToolError):
            recipes_units.delete_unit(mealie_client, item_id=unit["id"])


@pytest.fixture
def created_label(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel multi-purpose label and tear it down."""
    response = create_one_api_groups_labels_post.sync_detailed(
        client=mealie_client,
        body=MultiPurposeLabelCreate(name=f"{sentinel_name}-label"),
    )
    label = expect_dict("create_label", response)
    label_id = str(label["id"])
    try:
        yield {"id": label_id}
    finally:
        with contextlib.suppress(ToolError):
            expect_dict(
                "delete_label",
                delete_one_api_groups_labels_item_id_delete.sync_detailed(
                    label_id, client=mealie_client
                ),
            )


def _seed_food_and_label(
    client: AuthenticatedClient, item_id: str, food_id: str, label_id: str
) -> None:
    """Bind ``food_id`` and ``label_id`` to an item via a direct PUT.

    Neither field is exposed by ``add_shopping_list_item`` or
    ``update_shopping_list_item``, so a naive PUT during a partial update would
    overwrite them. The seed lets the lifecycle test assert they survive the
    update.
    """
    fetched = get_one_api_households_shopping_items_item_id_get.sync_detailed(
        item_id, client=client
    )
    current = expect_dict("seed_food_label", fetched)
    body = ShoppingListItemUpdate.from_dict(current)
    body.additional_properties = {}
    body.food_id = food_id
    body.label_id = label_id
    expect_dict(
        "seed_food_label",
        update_one_api_households_shopping_items_item_id_put.sync_detailed(
            item_id, client=client, body=body
        ),
    )


@pytest.mark.live
def test_shopping_list_item_lifecycle(
    mealie_client: AuthenticatedClient,
    created_food: dict[str, str],
    created_label: dict[str, str],
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    food_id = created_food["id"]
    label_id = created_label["id"]
    note = f"{sentinel_name}-item"

    added = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=note, quantity=3
    )
    item_id = added["id"]
    assert added["note"] == note
    assert added["quantity"] == 3
    assert added["checked"] is False

    # Bind food_id and label_id directly. Neither is exposed by the tools, so a
    # partial update via the tool must preserve them through fetch-then-merge.
    _seed_food_and_label(mealie_client, item_id, food_id=food_id, label_id=label_id)

    # Check the item off. note, quantity, food, and label must all survive the
    # PUT-replace: a merge that reset any of them would fail below.
    checked = households_shopping_list_items.update_shopping_list_item(
        mealie_client, item_id=item_id, checked=True
    )
    assert checked["checked"] is True
    assert checked["note"] == note
    assert checked["quantity"] == 3
    assert checked["foodId"] == food_id
    assert checked["labelId"] == label_id

    # Change only the quantity. The checked state, note, food, and label hold.
    requantified = households_shopping_list_items.update_shopping_list_item(
        mealie_client, item_id=item_id, quantity=5
    )
    assert requantified["quantity"] == 5
    assert requantified["checked"] is True
    assert requantified["note"] == note
    assert requantified["foodId"] == food_id
    assert requantified["labelId"] == label_id

    listing = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    found = next((i for i in listing["listItems"] if i["id"] == item_id), None)
    assert found is not None, f"item {item_id} not found on list {list_id}"
    assert found["quantity"] == 5
    assert found["foodId"] == food_id
    assert found["labelId"] == label_id

    ack = households_shopping_list_items.delete_shopping_list_item(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    after = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert all(i["id"] != item_id for i in after["listItems"])


@pytest.mark.live
def test_update_shopping_list_item_checkoff_drops_recipe_references(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """Checking an item off detaches its recipe references.

    Mealie clears a recipe-linked item's references server-side when the item
    is checked off, so a bought item no longer feeds recipe aggregation. The
    merged PUT body still carries the references; this pins the drop as Mealie
    behaviour rather than a merge regression, and guards the docstring claim
    against silent drift on a future Mealie version.
    """
    list_id = created_shopping_list["id"]
    recipe = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-recipe")
    try:
        recipe_id = recipe_crud.get_recipe(mealie_client, slug_or_id=recipe["slug"])["id"]
        updated_list = households_shopping_lists.add_recipe_to_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id
        )
        linked = next(
            (
                item
                for item in updated_list["listItems"]
                if any(ref["recipeId"] == recipe_id for ref in item["recipeReferences"])
            ),
            None,
        )
        assert linked is not None, f"no item linked to recipe {recipe_id}"
        assert linked["recipeReferences"] != []

        checked = households_shopping_list_items.update_shopping_list_item(
            mealie_client, item_id=linked["id"], checked=True
        )
        assert checked["checked"] is True
        assert checked["recipeReferences"] == []
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe["slug"])


@pytest.mark.live
def test_update_shopping_list_item_note_change_keeps_recipe_references(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """A non-checkoff update leaves a recipe-linked item's references intact.

    The checkoff drop is the documented exception; a note-only edit that does not
    check the item off must preserve its recipeReferences through the PUT-replace.
    """
    list_id = created_shopping_list["id"]
    recipe = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-recipe")
    try:
        recipe_id = recipe_crud.get_recipe(mealie_client, slug_or_id=recipe["slug"])["id"]
        updated_list = households_shopping_lists.add_recipe_to_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id
        )
        linked = next(
            (
                item
                for item in updated_list["listItems"]
                if any(ref["recipeId"] == recipe_id for ref in item["recipeReferences"])
            ),
            None,
        )
        assert linked is not None, f"no item linked to recipe {recipe_id}"

        renamed = households_shopping_list_items.update_shopping_list_item(
            mealie_client, item_id=linked["id"], note=f"{sentinel_name}-note"
        )
        assert renamed["checked"] is False
        after = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
        stored = next((i for i in after["listItems"] if i["id"] == linked["id"]), None)
        assert stored is not None, "linked item missing after update"
        assert [ref["recipeId"] for ref in stored["recipeReferences"]] == [recipe_id]
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe["slug"])


@pytest.mark.live
def test_add_shopping_list_item_defaults_quantity_to_one(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    added = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=created_shopping_list["id"], note=f"{sentinel_name}-item"
    )
    item_id = added["id"]
    try:
        # With quantity omitted, Mealie seeds 1 rather than 0 or null, and the
        # seed persists rather than only appearing on the add response.
        assert added["quantity"] == 1
        listing = households_shopping_lists.get_shopping_list(
            mealie_client, list_id=created_shopping_list["id"]
        )
        stored = next((i for i in listing["listItems"] if i["id"] == item_id), None)
        assert stored is not None, f"item {item_id} not found on the list"
        assert stored["quantity"] == 1
    finally:
        with contextlib.suppress(ToolError):
            households_shopping_list_items.delete_shopping_list_item(mealie_client, item_id=item_id)


@pytest.mark.live
def test_add_shopping_list_item_aggregates_items_sharing_food_and_unit(
    mealie_client: AuthenticatedClient,
    created_food: dict[str, str],
    created_unit: dict[str, str],
    created_label: dict[str, str],
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """A food and unit link is what makes Mealie merge a hand-added item.

    Two items carrying the same food and unit collapse into one line whose
    quantity is the sum; a free-text item with the same note does not. This is
    the behavioural difference the ids buy, so it also pins the ids as ids: a
    food or unit name in their place would not resolve.
    """
    list_id = created_shopping_list["id"]
    food_id = created_food["id"]
    unit_id = created_unit["id"]

    first = households_shopping_list_items.add_shopping_list_item(
        mealie_client,
        shopping_list_id=list_id,
        note=f"{sentinel_name}-butter",
        quantity=250,
        food_id=food_id,
        unit_id=unit_id,
        label_id=created_label["id"],
    )
    assert first["foodId"] == food_id
    assert first["unitId"] == unit_id
    assert first["labelId"] == created_label["id"]
    assert first["quantity"] == 250

    merged = households_shopping_list_items.add_shopping_list_item(
        mealie_client,
        shopping_list_id=list_id,
        note=f"{sentinel_name}-more-butter",
        quantity=250,
        food_id=food_id,
        unit_id=unit_id,
    )
    assert merged["id"] == first["id"]
    assert merged["quantity"] == 500

    free_text = households_shopping_list_items.add_shopping_list_item(
        mealie_client,
        shopping_list_id=list_id,
        note=f"{sentinel_name}-butter",
        quantity=250,
    )
    assert free_text["id"] != first["id"]

    stored = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert {i["id"] for i in stored["listItems"]} == {first["id"], free_text["id"]}


@pytest.mark.live
def test_update_shopping_list_item_sets_label(
    mealie_client: AuthenticatedClient,
    created_food: dict[str, str],
    created_unit: dict[str, str],
    created_label: dict[str, str],
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """Labelling an item leaves its other fields, including food and unit, alone."""
    note = f"{sentinel_name}-item"
    added = households_shopping_list_items.add_shopping_list_item(
        mealie_client,
        shopping_list_id=created_shopping_list["id"],
        note=note,
        quantity=2,
        food_id=created_food["id"],
        unit_id=created_unit["id"],
    )
    assert added["labelId"] is None

    updated = households_shopping_list_items.update_shopping_list_item(
        mealie_client, item_id=added["id"], label_id=created_label["id"]
    )
    assert updated["labelId"] == created_label["id"]
    assert updated["note"] == note
    assert updated["quantity"] == 2
    assert updated["foodId"] == created_food["id"]
    assert updated["unitId"] == created_unit["id"]


@pytest.mark.live
def test_add_shopping_list_items_fills_two_lists_in_one_call(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """Each bulk item names its own list, and an omitted quantity still seeds 1."""
    list_id = created_shopping_list["id"]
    other = households_shopping_lists.create_shopping_list(
        mealie_client, name=f"{sentinel_name}-other"
    )
    try:
        result = call_tool(
            "mealie_add_shopping_list_items",
            {
                "items": [
                    {
                        "shopping_list_id": list_id,
                        "note": f"{sentinel_name}-here",
                        "quantity": 4,
                    },
                    {"shopping_list_id": other["id"], "note": f"{sentinel_name}-there"},
                ]
            },
        )
        assert isinstance(result, dict)
        created = {item["note"]: item for item in result["createdItems"]}
        assert set(created) == {f"{sentinel_name}-here", f"{sentinel_name}-there"}
        assert created[f"{sentinel_name}-here"]["quantity"] == 4
        assert created[f"{sentinel_name}-there"]["quantity"] == 1

        here = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
        there = households_shopping_lists.get_shopping_list(mealie_client, list_id=other["id"])
        assert [i["id"] for i in here["listItems"]] == [created[f"{sentinel_name}-here"]["id"]]
        assert [i["id"] for i in there["listItems"]] == [created[f"{sentinel_name}-there"]["id"]]
    finally:
        with contextlib.suppress(ToolError):
            households_shopping_lists.delete_shopping_list(mealie_client, list_id=other["id"])


@pytest.mark.live
def test_add_shopping_list_items_maps_food_unit_and_label_per_entry(
    mealie_client: AuthenticatedClient,
    created_food: dict[str, str],
    created_unit: dict[str, str],
    created_label: dict[str, str],
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """Each entry's three ids reach Mealie on the field the caller named.

    The bulk path reads ``food_id``, ``unit_id``, and ``label_id`` out of the
    caller's dict and passes them positionally, so a swapped pair would land
    without an error. The food and unit ride on two entries and the label on a
    third, which makes a swap show up. Mealie's aggregation confirms the pair
    landed together: the two entries sharing a food and a unit collapse into one
    line with the summed quantity, so a batch can return fewer items than it was
    given.
    """
    list_id = created_shopping_list["id"]
    linked = {
        "shopping_list_id": list_id,
        "quantity": 250,
        "food_id": created_food["id"],
        "unit_id": created_unit["id"],
    }
    result = households_shopping_list_items.add_shopping_list_items(
        mealie_client,
        items=[
            {**linked, "note": f"{sentinel_name}-butter"},
            {**linked, "note": f"{sentinel_name}-more-butter"},
            {
                "shopping_list_id": list_id,
                "note": f"{sentinel_name}-labelled",
                "label_id": created_label["id"],
            },
        ],
    )
    created = result["createdItems"]
    assert len(created) == 2, f"expected the two linked entries to merge, got {created}"

    merged = next((i for i in created if i["foodId"] == created_food["id"]), None)
    assert merged is not None, "no created item carries the food link"
    assert merged["unitId"] == created_unit["id"]
    assert merged["labelId"] is None
    assert merged["quantity"] == 500

    labelled = next((i for i in created if i["id"] != merged["id"]), None)
    assert labelled is not None, "the labelled entry is missing"
    assert labelled["labelId"] == created_label["id"]
    assert labelled["foodId"] is None
    assert labelled["unitId"] is None

    stored = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert {i["id"] for i in stored["listItems"]} == {i["id"] for i in created}


@pytest.mark.live
def test_add_shopping_list_items_keeps_the_items_written_before_a_failure(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """The bulk create is not atomic, as the tool docstring warns.

    The second item names a UUID that is no shopping list, which Mealie answers
    with a 500 after it has already written the first item.
    """
    list_id = created_shopping_list["id"]
    with pytest.raises(ToolError):
        households_shopping_list_items.add_shopping_list_items(
            mealie_client,
            items=[
                {"shopping_list_id": list_id, "note": f"{sentinel_name}-written"},
                {"shopping_list_id": ABSENT_UUID, "note": f"{sentinel_name}-rejected"},
            ],
        )

    stored = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert [i["note"] for i in stored["listItems"]] == [f"{sentinel_name}-written"]


@pytest.mark.live
def test_update_shopping_list_items_checks_off_several_and_keeps_links(
    mealie_client: AuthenticatedClient,
    created_food: dict[str, str],
    created_unit: dict[str, str],
    created_shopping_list: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """One bulk call checks off several items without clobbering their links.

    The bulk endpoint PUT-replaces every item in the body, so the food and unit
    links, which the tool does not expose, only survive because each item is
    merged from its current state first.
    """
    list_id = created_shopping_list["id"]
    linked = households_shopping_list_items.add_shopping_list_item(
        mealie_client,
        shopping_list_id=list_id,
        note=f"{sentinel_name}-linked",
        quantity=250,
        food_id=created_food["id"],
        unit_id=created_unit["id"],
    )
    plain = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-plain", quantity=2
    )

    result = call_tool(
        "mealie_update_shopping_list_items",
        {
            "items": [
                {"id": linked["id"], "checked": True},
                {"id": plain["id"], "checked": True, "note": f"{sentinel_name}-renamed"},
            ]
        },
    )
    assert isinstance(result, dict)
    updated = {item["id"]: item for item in result["updatedItems"]}
    assert set(updated) == {linked["id"], plain["id"]}
    assert updated[linked["id"]]["note"] == f"{sentinel_name}-linked"
    assert updated[linked["id"]]["quantity"] == 250
    assert updated[linked["id"]]["foodId"] == created_food["id"]
    assert updated[linked["id"]]["unitId"] == created_unit["id"]
    assert updated[plain["id"]]["note"] == f"{sentinel_name}-renamed"

    stored = {
        item["id"]: item
        for item in households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)[
            "listItems"
        ]
    }
    assert stored[linked["id"]]["checked"] is True
    assert stored[linked["id"]]["foodId"] == created_food["id"]
    assert stored[linked["id"]]["unitId"] == created_unit["id"]
    assert stored[plain["id"]]["checked"] is True


@pytest.mark.live
def test_update_shopping_list_items_merges_an_unchecked_item_into_its_twin(
    mealie_client: AuthenticatedClient,
    created_food: dict[str, str],
    created_unit: dict[str, str],
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """A checked item stands apart until it is unchecked, then Mealie merges it.

    This is why the bulk response reports deleted items: an update that changes
    nothing but a checked flag can still remove a line from the list.
    """
    list_id = created_shopping_list["id"]
    first = households_shopping_list_items.add_shopping_list_item(
        mealie_client,
        shopping_list_id=list_id,
        note=f"{sentinel_name}-first",
        quantity=250,
        food_id=created_food["id"],
        unit_id=created_unit["id"],
    )
    households_shopping_list_items.update_shopping_list_item(
        mealie_client, item_id=first["id"], checked=True
    )

    second = households_shopping_list_items.add_shopping_list_item(
        mealie_client,
        shopping_list_id=list_id,
        note=f"{sentinel_name}-second",
        quantity=250,
        food_id=created_food["id"],
        unit_id=created_unit["id"],
    )
    assert second["id"] != first["id"], "a checked item must not absorb a new one"

    result = households_shopping_list_items.update_shopping_list_items(
        mealie_client, items=[{"id": first["id"], "checked": False}]
    )
    assert [item["id"] for item in result["deletedItems"]] == [first["id"]]
    assert [item["id"] for item in result["updatedItems"]] == [second["id"]]
    assert result["updatedItems"][0]["quantity"] == 500

    stored = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert [i["id"] for i in stored["listItems"]] == [second["id"]]


@pytest.mark.live
def test_update_shopping_list_items_writes_nothing_when_an_id_is_unknown(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    """Reading every item before the write is what keeps a bad batch off the list."""
    note = f"{sentinel_name}-item"
    added = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=created_shopping_list["id"], note=note
    )
    with pytest.raises(ToolError):
        households_shopping_list_items.update_shopping_list_items(
            mealie_client,
            items=[
                {"id": added["id"], "note": f"{sentinel_name}-renamed"},
                {"id": ABSENT_UUID, "checked": True},
            ],
        )

    stored = households_shopping_lists.get_shopping_list(
        mealie_client, list_id=created_shopping_list["id"]
    )
    assert [i["note"] for i in stored["listItems"]] == [note]


@pytest.mark.live
def test_list_shopping_list_items_includes_sentinel(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    note = f"{sentinel_name}-item"
    added = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=note
    )
    item_id = added["id"]
    try:
        envelope = households_shopping_list_items.list_shopping_list_items(
            mealie_client, per_page=100
        )
        found = next((i for i in envelope["items"] if i["id"] == item_id), None)
        assert found is not None, f"item {item_id} not found across shopping lists"
        assert found["note"] == note
    finally:
        with contextlib.suppress(ToolError):
            households_shopping_list_items.delete_shopping_list_item(mealie_client, item_id=item_id)


@pytest.mark.live
def test_delete_shopping_list_items_bulk_removes_all(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    list_id = created_shopping_list["id"]
    first = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-item-1"
    )
    second = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-item-2"
    )
    item_ids = [first["id"], second["id"]]
    try:
        ack = call_tool("mealie_delete_shopping_list_items_bulk", {"item_ids": item_ids})
        assert ack == {"ids": item_ids, "deleted": True}

        after = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
        remaining = {i["id"] for i in after["listItems"]}
        assert remaining.isdisjoint(item_ids)
    finally:
        for item_id in item_ids:
            with contextlib.suppress(ToolError):
                households_shopping_list_items.delete_shopping_list_item(
                    mealie_client, item_id=item_id
                )


@pytest.mark.live
def test_add_shopping_list_item_round_trips_through_wrapper(
    created_shopping_list: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    note = f"{sentinel_name}-item"
    added = call_tool(
        "mealie_add_shopping_list_item",
        {"shopping_list_id": created_shopping_list["id"], "note": note, "quantity": 3},
    )
    assert isinstance(added, dict)
    item_id = added["id"]
    try:
        assert added["note"] == note
        assert added["quantity"] == 3
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_shopping_list_item", {"item_id": item_id})
