"""Live test for the household shopping list lifecycle.

Stages a sentinel shopping list, exercises the get, list, rename, and delete
tools, and asserts the rename preserves the list's items. Two sentinel items
are added before the rename so a regression in fetch-then-merge, which would
clobber ``listItems`` on the PUT-replace, fails the test. Cleanup runs even when
the body fails so no `mcp-test-` data lingers.
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
    """Create a sentinel shopping list and tear it down."""
    created = households_shopping_lists.create_shopping_list(mealie_client, name=sentinel_name)
    list_id = created["id"]
    try:
        yield {"id": list_id}
    finally:
        with contextlib.suppress(ToolError):
            households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)


@pytest.mark.live
def test_shopping_list_lifecycle(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]

    fetched = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert fetched["id"] == list_id
    assert fetched["name"] == sentinel_name

    listing = households_shopping_lists.list_shopping_lists(mealie_client, per_page=100)
    assert any(item["id"] == list_id for item in listing["items"])

    # Add two items so the rename has list state that must survive the PUT-replace.
    first = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-a"
    )
    second = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-b"
    )

    # Rename. The items are not supplied to the rename tool, so they must be
    # preserved by fetch-then-merge rather than cleared.
    new_name = f"{sentinel_name}-renamed"
    renamed = households_shopping_lists.update_shopping_list(
        mealie_client, list_id=list_id, name=new_name
    )
    assert renamed["name"] == new_name

    after = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert after["name"] == new_name
    surviving = {item["id"]: item for item in after["listItems"]}
    assert first["id"] in surviving
    assert second["id"] in surviving
    # The items keep their notes, not just their ids: a merge that reset item
    # fields while preserving ids would still fail here.
    assert surviving[first["id"]]["note"] == f"{sentinel_name}-a"
    assert surviving[second["id"]]["note"] == f"{sentinel_name}-b"

    ack = households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)
    assert ack == {"id": list_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_shopping_list failed \(404"):
        households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
