"""Household shopping list item tools.

Mirrors `mealie_mcp.client.api.households_shopping_list_items`. Exposes the
per-item lifecycle on a shopping list: add a free-text item, update an item
(toggle checked, edit quantity or note), and remove an item. Bulk operations
and recipe-derived items are out of scope. The lists themselves live in
`households_shopping_lists`.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_shopping_list_items import (
    create_one_api_households_shopping_items_post,
    delete_one_api_households_shopping_items_item_id_delete,
    get_one_api_households_shopping_items_item_id_get,
    update_one_api_households_shopping_items_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.shopping_list_item_create import ShoppingListItemCreate
from mealie_mcp.client.models.shopping_list_item_update import ShoppingListItemUpdate
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    decode,
    expect_dict,
    raise_api_error,
    require_non_empty,
    to_unset,
)


def _single_item(action: str, response: Any, key: str) -> dict[str, Any]:
    """Pull the one changed item out of a bulk-collection response.

    The create and update endpoints return a `ShoppingListItemsCollectionOut`
    envelope with ``createdItems``/``updatedItems``/``deletedItems`` arrays even
    for a single change. The tools operate on one item, so the matching array's
    sole entry is unwrapped for a stable single-item contract.
    """
    payload = decode(response.content)
    if not isinstance(payload, dict):
        raise ToolError(f"Unexpected {action} response: {payload!r}")
    items = payload.get(key)
    if not isinstance(items, list) or not items:
        raise ToolError(f"Mealie {action} returned no {key}")
    item = items[0]
    if not isinstance(item, dict):
        raise ToolError(f"Unexpected {action} item shape: {item!r}")
    return item


def add_shopping_list_item(
    client: AuthenticatedClient,
    shopping_list_id: str,
    note: str,
    quantity: float | None = None,
) -> dict[str, Any]:
    """Add a free-text item to a shopping list. Returns the new item payload."""
    require_non_empty("shopping_list_id", shopping_list_id)
    require_non_empty("note", note)
    body = ShoppingListItemCreate(
        shopping_list_id=shopping_list_id,
        note=note,
        quantity=to_unset(quantity),
    )
    response = create_one_api_households_shopping_items_post.sync_detailed(client=client, body=body)
    if response.status_code != HTTPStatus.CREATED:
        raise_api_error("add_shopping_list_item", int(response.status_code), response.content)
    return _single_item("add_shopping_list_item", response, "createdItems")


def update_shopping_list_item(
    client: AuthenticatedClient,
    item_id: str,
    *,
    note: str | None = None,
    quantity: float | None = None,
    checked: bool | None = None,
) -> dict[str, Any]:
    """Update a shopping list item. Returns the updated item payload.

    The endpoint PUT-replaces the item, and the body model defaults most fields
    to concrete values rather than leaving them unset. The current item is
    therefore fetched and the body rebuilt from it, so unsupplied fields and the
    item's food, unit, label, and recipe links keep their current values; only
    the caller's edits are applied on top.
    """
    require_non_empty("item_id", item_id)
    if note is None and quantity is None and checked is None:
        raise ToolError("update_shopping_list_item requires at least one field to update")

    fetched = get_one_api_households_shopping_items_item_id_get.sync_detailed(
        item_id, client=client
    )
    current = expect_dict("update_shopping_list_item", fetched)
    body = ShoppingListItemUpdate.from_dict(current)
    body.additional_properties = {}
    if note is not None:
        body.note = note
    if quantity is not None:
        body.quantity = quantity
    if checked is not None:
        body.checked = checked
    response = update_one_api_households_shopping_items_item_id_put.sync_detailed(
        item_id, client=client, body=body
    )
    if response.status_code != HTTPStatus.OK:
        raise_api_error("update_shopping_list_item", int(response.status_code), response.content)
    return _single_item("update_shopping_list_item", response, "updatedItems")


def delete_shopping_list_item(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a shopping list item by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)
    response = delete_one_api_households_shopping_items_item_id_delete.sync_detailed(
        item_id, client=client
    )
    return ack_delete("delete_shopping_list_item", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the household shopping list item tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_add_shopping_list_item")
    def _add_shopping_list_item(
        shopping_list_id: str,
        note: str,
        quantity: float | None = None,
    ) -> dict[str, Any]:
        """Add a free-text item to a shopping list.

        The item is described by ``note`` (the text shown on the list), with an
        optional ``quantity``. Food, unit, and recipe associations are not set
        through this tool.

        Args:
            shopping_list_id: UUID of the shopping list to add to.
            note: Free-text description of the item. Required.
            quantity: Optional amount. Defaults to 1 in Mealie when omitted.

        Returns:
            The newly created shopping list item as a JSON-compatible dict.
        """
        return add_shopping_list_item(
            get_client(),
            shopping_list_id=shopping_list_id,
            note=note,
            quantity=quantity,
        )

    @mcp.tool(name="mealie_update_shopping_list_item")
    def _update_shopping_list_item(
        item_id: str,
        note: str | None = None,
        quantity: float | None = None,
        checked: bool | None = None,
    ) -> dict[str, Any]:
        """Edit a shopping list item, or check it off.

        Only the fields supplied change; omitted fields keep their current value
        and the item's food, unit, and label links are preserved. At least one
        of ``note``, ``quantity``, or ``checked`` must be provided.

        Args:
            item_id: UUID of the shopping list item.
            note: New free-text description.
            quantity: New amount.
            checked: ``True`` to mark the item bought, ``False`` to uncheck it.

        Returns:
            The updated shopping list item as a JSON-compatible dict.
        """
        return update_shopping_list_item(
            get_client(),
            item_id=item_id,
            note=note,
            quantity=quantity,
            checked=checked,
        )

    @mcp.tool(name="mealie_delete_shopping_list_item")
    def _delete_shopping_list_item(item_id: str) -> dict[str, Any]:
        """Delete an item from a shopping list by id.

        Args:
            item_id: UUID of the shopping list item to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_shopping_list_item(get_client(), item_id=item_id)
