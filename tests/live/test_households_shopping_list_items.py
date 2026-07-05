"""Live test for the household shopping list item lifecycle.

Stages a sentinel shopping list, adds a sentinel item, seeds ``food_id`` and
``label_id`` (both unexposed by the update tool), then exercises the update and
delete tools. The partial updates change one field at a time and assert that
the unsupplied fields and the seeded food/label links survive the PUT-replace,
so a regression in fetch-then-merge fails the test. The test signature requests
the list fixture last so pytest tears the list (and cascades its items) down
before the label and food, and cleanup runs even when the body fails so no
`mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator

import httpx
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
    recipes_foods,
)
from mealie_mcp.tools._common import expect_dict


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
        with contextlib.suppress(httpx.HTTPError):
            delete_one_api_groups_labels_item_id_delete.sync_detailed(
                label_id, client=mealie_client
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
