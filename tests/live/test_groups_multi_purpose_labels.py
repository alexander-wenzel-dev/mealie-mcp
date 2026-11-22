"""Live tests for the multi purpose label lifecycle, the empty list, and the merge.

Stages a sentinel label and exercises create, get, list, update, and delete. The
lifecycle test proves a non-default ``color`` round-trips on create and survives
a name-only update, the clobber proof for the update tool's fetch-then-merge:
``color`` is absent from a name-only PUT body, so a sparse update would reset it
to Mealie's ``#959595`` default. The empty-list and merge tests stage foods
and a shopping list carrying the labels. Cleanup runs even when the body fails so no
`mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import (
    groups_multi_purpose_labels,
    households_shopping_list_items,
    households_shopping_lists,
    recipes_foods,
)


def _list_item(client: AuthenticatedClient, list_id: str, item_id: str) -> dict[str, Any]:
    """Read one item back off its shopping list."""
    items = households_shopping_lists.get_shopping_list(client, list_id=list_id)["listItems"]
    found = next((entry for entry in items if entry["id"] == item_id), None)
    assert found is not None, f"shopping list item {item_id} is not on list {list_id}"
    return dict(found)


@pytest.mark.live
def test_label_lifecycle_color_survives_name_only_update(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    color = "#123456"
    item_id: str | None = None
    try:
        created = groups_multi_purpose_labels.create_label(
            mealie_client, name=sentinel_name, color=color
        )
        item_id = created["id"]

        fetched = groups_multi_purpose_labels.get_label(mealie_client, item_id=item_id)
        assert fetched["name"] == sentinel_name
        assert fetched["color"] == color

        listing = groups_multi_purpose_labels.list_labels(mealie_client, per_page=100)
        assert any(item["id"] == item_id for item in listing["items"])

        new_name = f"{sentinel_name}-renamed"
        updated = groups_multi_purpose_labels.update_label(
            mealie_client, item_id=item_id, name=new_name
        )
        assert updated["name"] == new_name

        # A name-only update must not clobber the non-default color: fetch-then-merge
        # preserves it through the PUT-replace instead of resetting it to #959595.
        refetched = groups_multi_purpose_labels.get_label(mealie_client, item_id=item_id)
        assert refetched["name"] == new_name
        assert refetched["color"] == color

        ack = groups_multi_purpose_labels.delete_label(mealie_client, item_id=item_id)
        assert ack == {"id": item_id, "deleted": True}
        deleted_id, item_id = item_id, None

        with pytest.raises(ToolError, match=r"Mealie get_label failed \(404"):
            groups_multi_purpose_labels.get_label(mealie_client, item_id=deleted_id)
    finally:
        if item_id is not None:
            with contextlib.suppress(ToolError):
                groups_multi_purpose_labels.delete_label(mealie_client, item_id=item_id)


@pytest.mark.live
def test_create_label_defaults_color_to_gray(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    created = groups_multi_purpose_labels.create_label(mealie_client, name=sentinel_name)
    item_id = created["id"]
    try:
        # With color omitted, Mealie seeds the documented #959595 default rather
        # than leaving it empty.
        assert created["color"] == "#959595"
        fetched = groups_multi_purpose_labels.get_label(mealie_client, item_id=item_id)
        assert fetched["color"] == "#959595"
    finally:
        with contextlib.suppress(ToolError):
            groups_multi_purpose_labels.delete_label(mealie_client, item_id=item_id)


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_create_label_round_trips_color_through_wrapper(
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    color = "#abcdef"
    created = call_tool("mealie_create_label", {"name": sentinel_name, "color": color})
    assert isinstance(created, dict)
    item_id = created["id"]
    try:
        # name and color are both str; fetching both back catches a wrapper swap.
        fetched = call_tool("mealie_get_label", {"item_id": item_id})
        assert isinstance(fetched, dict)
        assert fetched["name"] == sentinel_name
        assert fetched["color"] == color
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_label", {"item_id": item_id})


@pytest.mark.live
def test_empty_labels_drop_a_label_once_a_food_or_an_item_uses_it(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    label_ids: list[str] = []
    food_id: str | None = None
    list_id: str | None = None
    try:
        for suffix in ("food", "item"):
            label = groups_multi_purpose_labels.create_label(
                mealie_client, name=f"{sentinel_name}-{suffix}"
            )
            label_ids.append(str(label["id"]))
        food_label_id, item_label_id = label_ids
        empty = {
            entry["id"] for entry in groups_multi_purpose_labels.list_empty_labels(mealie_client)
        }
        assert {food_label_id, item_label_id} <= empty

        food_id = str(
            recipes_foods.create_food(
                mealie_client, name=f"{sentinel_name}-food", label_id=food_label_id
            )["id"]
        )
        list_id = str(
            households_shopping_lists.create_shopping_list(
                mealie_client, name=f"{sentinel_name}-list"
            )["id"]
        )
        households_shopping_list_items.add_shopping_list_item(
            mealie_client,
            shopping_list_id=list_id,
            note=f"{sentinel_name}-item",
            label_id=item_label_id,
        )

        empty = {
            entry["id"] for entry in groups_multi_purpose_labels.list_empty_labels(mealie_client)
        }
        assert food_label_id not in empty
        assert item_label_id not in empty
    finally:
        if list_id is not None:
            with contextlib.suppress(ToolError):
                households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)
        if food_id is not None:
            with contextlib.suppress(ToolError):
                recipes_foods.delete_food(mealie_client, item_id=food_id)
        for label_id in label_ids:
            with contextlib.suppress(ToolError):
                groups_multi_purpose_labels.delete_label(mealie_client, item_id=label_id)


@pytest.mark.live
def test_merge_label_repoints_foods_and_items_and_deletes_the_source(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """The merge moves foods and items to the target and drops the source.

    The merge runs through the wrapper because both arguments are ids of the
    same type, where a swapped forward would delete the surviving label.
    """
    label_ids: list[str] = []
    food_id: str | None = None
    list_id: str | None = None
    try:
        for suffix in ("source", "target"):
            label = groups_multi_purpose_labels.create_label(
                mealie_client, name=f"{sentinel_name}-{suffix}"
            )
            label_ids.append(str(label["id"]))
        source_id, target_id = label_ids
        food_id = str(
            recipes_foods.create_food(
                mealie_client, name=f"{sentinel_name}-food", label_id=source_id
            )["id"]
        )
        list_id = str(
            households_shopping_lists.create_shopping_list(
                mealie_client, name=f"{sentinel_name}-list"
            )["id"]
        )
        item_id = str(
            households_shopping_list_items.add_shopping_list_item(
                mealie_client,
                shopping_list_id=list_id,
                note=f"{sentinel_name}-item",
                label_id=source_id,
            )["id"]
        )
        # Mealie gives every list an entry for every label, so the list holds
        # both and the merge takes the branch that drops the source's entry.
        staged = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
        positions = {entry["labelId"]: entry["position"] for entry in staged["labelSettings"]}
        assert {source_id, target_id} <= positions.keys()

        survivor = call_tool(
            "mealie_merge_label", {"from_label_id": source_id, "to_label_id": target_id}
        )
        assert isinstance(survivor, dict)
        assert survivor["id"] == target_id

        assert recipes_foods.get_food(mealie_client, item_id=food_id)["labelId"] == target_id
        assert _list_item(mealie_client, list_id, item_id)["labelId"] == target_id
        merged = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
        merged_positions = {
            entry["labelId"]: entry["position"] for entry in merged["labelSettings"]
        }
        assert source_id not in merged_positions
        assert merged_positions[target_id] == positions[target_id]
        with pytest.raises(ToolError, match=r"Mealie get_label failed \(404"):
            groups_multi_purpose_labels.get_label(mealie_client, item_id=source_id)
    finally:
        if list_id is not None:
            with contextlib.suppress(ToolError):
                households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)
        if food_id is not None:
            with contextlib.suppress(ToolError):
                recipes_foods.delete_food(mealie_client, item_id=food_id)
        for label_id in label_ids:
            with contextlib.suppress(ToolError):
                groups_multi_purpose_labels.delete_label(mealie_client, item_id=label_id)
