"""Live test for the household shopping list lifecycle.

Stages a sentinel shopping list, exercises the get, list, rename, and delete
tools, and asserts the rename preserves the list's items and extras. Two items
and an extras key are seeded before the rename, so a regression in
fetch-then-merge would clobber either ``listItems`` or ``extras`` on the
PUT-replace and fail the test. Cleanup runs even when the body fails so no
`mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_shopping_lists import (
    update_one_api_households_shopping_lists_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.shopping_list_update import ShoppingListUpdate
from mealie_mcp.client.models.shopping_list_update_extras_type_0 import (
    ShoppingListUpdateExtrasType0,
)
from mealie_mcp.tools import households_shopping_list_items, households_shopping_lists
from mealie_mcp.tools._common import expect_dict


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


def _seed_extras(client: AuthenticatedClient, list_id: str, *, key: str, value: str) -> None:
    """Set a non-default ``extras`` entry on a list via a direct PUT.

    ``extras`` is not exposed by ``update_shopping_list``, so a naive PUT would
    overwrite it. Seeding it here lets the lifecycle test assert it survives the
    rename, alongside the seeded items.
    """
    fetched = households_shopping_lists.get_shopping_list(client, list_id=list_id)
    extras_seed = ShoppingListUpdateExtrasType0()
    extras_seed[key] = value
    body = ShoppingListUpdate(
        group_id=fetched["groupId"],
        user_id=fetched["userId"],
        id=list_id,
        name=fetched["name"],
        extras=extras_seed,
    )
    expect_dict(
        "seed_extras",
        update_one_api_households_shopping_lists_item_id_put.sync_detailed(
            list_id, client=client, body=body
        ),
    )


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

    # Seed two unexposed body-model fields: extras (via a direct PUT on the
    # list endpoint) and listItems (via the dedicated items endpoint, which is
    # a separate POST and does not touch the list body). A merge regression on
    # either during the rename would fail below.
    extras_key = f"extras_{sentinel_name.replace('-', '_')}"
    extras_value = f"{sentinel_name}-extras"
    _seed_extras(mealie_client, list_id, key=extras_key, value=extras_value)
    first = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-a"
    )
    second = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-b"
    )

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
    assert after["extras"][extras_key] == extras_value

    ack = households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)
    assert ack == {"id": list_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_shopping_list failed \(404"):
        households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
