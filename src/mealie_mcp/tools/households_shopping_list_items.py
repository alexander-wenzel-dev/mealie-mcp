"""Household shopping list item tools.

Mirrors `mealie_mcp.client.api.households_shopping_list_items`. Exposes the
per-item lifecycle on a shopping list: list items across the household's
lists, add a free-text item, update an item (toggle checked, edit quantity or
note), remove an item, and delete several items in one call. Bulk create and
bulk update, and recipe-derived items, are out of scope. The lists themselves
live in `households_shopping_lists`.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_shopping_list_items import (
    create_one_api_households_shopping_items_post,
    delete_many_api_households_shopping_items_delete,
    delete_one_api_households_shopping_items_item_id_delete,
    get_all_api_households_shopping_items_get,
    get_one_api_households_shopping_items_item_id_get,
    update_one_api_households_shopping_items_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.shopping_list_item_create import ShoppingListItemCreate
from mealie_mcp.client.models.shopping_list_item_update import ShoppingListItemUpdate
from mealie_mcp.client.types import Response
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    ack_delete_bulk,
    decode,
    expect_dict,
    parse_order_direction,
    raise_api_error,
    require_non_empty,
    require_pagination,
    to_unset,
)


def _single_item(action: str, response: Response[Any], key: str) -> dict[str, Any]:
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


def list_shopping_list_items(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List shopping list items across the household's lists, paginated."""
    require_pagination(page, per_page)
    response = get_all_api_households_shopping_items_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_shopping_list_items", response)


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
    item's food, unit, and label links keep their current values; only the
    caller's edits are applied on top. Recipe links are the exception: Mealie
    drops an item's recipe references server-side when the update checks it off,
    regardless of the merged body.
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


def delete_shopping_list_items_bulk(
    client: AuthenticatedClient, item_ids: list[str]
) -> dict[str, Any]:
    """Delete several shopping list items in one call.

    The endpoint returns a ``SuccessResponse`` envelope rather than a per-id
    result, so the tool returns a canonical batch acknowledgement
    ``{"ids": item_ids, "deleted": True}`` after verifying the 200 response.
    """
    if not item_ids:
        raise ToolError("item_ids must contain at least one id")
    for item_id in item_ids:
        require_non_empty("item_id", item_id)
    response = delete_many_api_households_shopping_items_delete.sync_detailed(
        client=client, ids=item_ids
    )
    return ack_delete_bulk("delete_shopping_list_items_bulk", response, item_ids)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the household shopping list item tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_shopping_list_items")
    def _list_shopping_list_items(
        page: int = 1,
        per_page: int = 50,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List shopping list items across all of the household's lists, paginated.

        The items span every list in the household, not one list. To read the
        items of a single list, use ``mealie_get_shopping_list`` instead.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            order_by: Optional column name to sort on (e.g. ``"created_at"``).
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_shopping_list_items(
            get_client(),
            page=page,
            per_page=per_page,
            order_by=order_by,
            order_direction=order_direction,
        )

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
        and the item's food, unit, and label links are preserved. Checking an
        item off additionally drops its recipe links, which Mealie clears
        server-side. At least one of ``note``, ``quantity``, or ``checked`` must
        be provided.

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

    @mcp.tool(name="mealie_delete_shopping_list_items_bulk")
    def _delete_shopping_list_items_bulk(item_ids: list[str]) -> dict[str, Any]:
        """Delete several shopping list items in one call.

        Deletes every item whose id is in ``item_ids`` with a single request,
        rather than one request per item. The list must be non-empty and every
        id non-blank. Mealie returns a success envelope, not a per-id result,
        so the acknowledgement reflects the ids requested, not a confirmation
        of each.

        Args:
            item_ids: UUIDs of the shopping list items to delete. Required,
                non-empty, each id non-blank.

        Returns:
            A canonical batch acknowledgement ``{"ids": <item_ids>, "deleted": True}``.
        """
        return delete_shopping_list_items_bulk(get_client(), item_ids=item_ids)
