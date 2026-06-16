"""Live test for the household shopping list item lifecycle.

Stages a sentinel shopping list, adds a sentinel item, then exercises the
update and remove tools. The update steps change one field at a time and assert
the unsupplied fields survive, so a regression in fetch-then-merge, which would
reset ``note`` and ``quantity`` to their schema defaults on the PUT-replace,
fails the test. Cleanup deletes the list, which removes its items, and runs even
when the body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_shopping_list_items, households_shopping_lists


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


@pytest.mark.live
def test_shopping_list_item_lifecycle(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    note = f"{sentinel_name}-item"

    added = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=note, quantity=3
    )
    item_id = added["id"]
    assert added["note"] == note
    assert added["quantity"] == 3
    assert added["checked"] is False

    # Check the item off. note and quantity are not supplied, so fetch-then-merge
    # must preserve them rather than reset to the schema defaults '' and 1.
    checked = households_shopping_list_items.update_shopping_list_item(
        mealie_client, item_id=item_id, checked=True
    )
    assert checked["checked"] is True
    assert checked["note"] == note
    assert checked["quantity"] == 3

    # Change only the quantity. The checked state and note must hold.
    requantified = households_shopping_list_items.update_shopping_list_item(
        mealie_client, item_id=item_id, quantity=5
    )
    assert requantified["quantity"] == 5
    assert requantified["checked"] is True
    assert requantified["note"] == note

    # The item is visible on the parent list.
    listing = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    found = next((i for i in listing["listItems"] if i["id"] == item_id), None)
    assert found is not None, f"item {item_id} not found on list {list_id}"
    assert found["quantity"] == 5

    ack = households_shopping_list_items.remove_shopping_list_item(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    after = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert all(i["id"] != item_id for i in after["listItems"])
