"""Household shopping list item tools.

Mirrors `mealie_mcp.client.api.households_shopping_list_items`. Exposes the
per-item lifecycle on a shopping list: list items across the household's
lists, add an item, update an item (toggle checked, edit quantity, note, or
label), remove an item, and create, update, or delete several items in one
call. Recipe-derived items are out of scope. The lists themselves live in
`households_shopping_lists`.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_shopping_list_items import (
    create_many_api_households_shopping_items_create_bulk_post,
    create_one_api_households_shopping_items_post,
    delete_many_api_households_shopping_items_delete,
    delete_one_api_households_shopping_items_item_id_delete,
    get_all_api_households_shopping_items_get,
    get_one_api_households_shopping_items_item_id_get,
    update_many_api_households_shopping_items_put,
    update_one_api_households_shopping_items_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.shopping_list_item_create import ShoppingListItemCreate
from mealie_mcp.client.models.shopping_list_item_update import ShoppingListItemUpdate
from mealie_mcp.client.models.shopping_list_item_update_bulk import ShoppingListItemUpdateBulk
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

CREATE_ITEM_FIELDS = ("shopping_list_id", "note", "quantity", "food_id", "unit_id", "label_id")
UPDATE_ITEM_FIELDS = ("id", "note", "quantity", "checked", "label_id")


def _single_item(action: str, response: Response[Any], keys: tuple[str, ...]) -> dict[str, Any]:
    """Pull the one changed item out of a bulk-collection response.

    The create and update endpoints return a `ShoppingListItemsCollectionOut`
    envelope with ``createdItems``/``updatedItems``/``deletedItems`` arrays even
    for a single change. The tools operate on one item, so the first non-empty
    array in ``keys`` yields the entry that is unwrapped for a stable
    single-item contract. An add that Mealie aggregates into a matching item
    reports the merged item under ``updatedItems`` and creates nothing, so the
    add path reads both keys.
    """
    payload = decode(response.content)
    if not isinstance(payload, dict):
        raise ToolError(f"Unexpected {action} response: {payload!r}")
    for key in keys:
        items = payload.get(key)
        if isinstance(items, list) and items:
            item = items[0]
            if not isinstance(item, dict):
                raise ToolError(f"Unexpected {action} item shape: {item!r}")
            return item
    raise ToolError(f"Mealie {action} returned no {' or '.join(keys)}")


def _item_string(action: str, index: int, item: dict[str, Any], field: str) -> str:
    """Return a required string field of a bulk item, or raise `ToolError`."""
    value = item.get(field)
    if not isinstance(value, str):
        raise ToolError(f"{action} items[{index}].{field} must be a non-empty string")
    require_non_empty(f"items[{index}].{field}", value)
    return value


def _require_item_fields(action: str, index: int, item: Any, allowed: tuple[str, ...]) -> None:
    """Reject a bulk item that is not an object or carries a field the tool cannot send."""
    if not isinstance(item, dict):
        raise ToolError(f"{action} items[{index}] must be an object")
    unsupported = sorted(set(item) - set(allowed))
    if unsupported:
        raise ToolError(
            f"{action} items[{index}] has unsupported fields {unsupported}; "
            f"supported fields are {list(allowed)}"
        )


def _create_body(
    shopping_list_id: str,
    note: str,
    quantity: float | None,
    food_id: str | None,
    unit_id: str | None,
    label_id: str | None,
) -> ShoppingListItemCreate:
    """Build the create body shared by the single-item and bulk add paths."""
    return ShoppingListItemCreate(
        shopping_list_id=shopping_list_id,
        note=note,
        quantity=to_unset(quantity),
        food_id=to_unset(food_id),
        unit_id=to_unset(unit_id),
        label_id=to_unset(label_id),
    )


def _apply_item_edits(
    body: ShoppingListItemUpdate | ShoppingListItemUpdateBulk,
    note: str | None = None,
    quantity: float | None = None,
    checked: bool | None = None,
    label_id: str | None = None,
) -> None:
    """Apply the supplied edits onto a body merged from the item's current state."""
    if note is not None:
        body.note = note
    if quantity is not None:
        body.quantity = quantity
    if checked is not None:
        body.checked = checked
    if label_id is not None:
        # Mealie parses labelId as a UUID and rejects "", so the clear travels
        # as JSON null.
        body.label_id = label_id or None


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
    food_id: str | None = None,
    unit_id: str | None = None,
    label_id: str | None = None,
) -> dict[str, Any]:
    """Add an item to a shopping list. Returns the new or merged item payload."""
    require_non_empty("shopping_list_id", shopping_list_id)
    require_non_empty("note", note)
    body = _create_body(shopping_list_id, note, quantity, food_id, unit_id, label_id)
    response = create_one_api_households_shopping_items_post.sync_detailed(client=client, body=body)
    if response.status_code != HTTPStatus.CREATED:
        raise_api_error("add_shopping_list_item", int(response.status_code), response.content)
    return _single_item("add_shopping_list_item", response, ("createdItems", "updatedItems"))


def add_shopping_list_items(
    client: AuthenticatedClient, items: list[dict[str, Any]]
) -> dict[str, Any]:
    """Create several shopping list items in one call. Returns the collection envelope."""
    action = "add_shopping_list_items"
    if not items:
        raise ToolError("items must contain at least one item")
    bodies = []
    for index, item in enumerate(items):
        _require_item_fields(action, index, item, CREATE_ITEM_FIELDS)
        bodies.append(
            _create_body(
                _item_string(action, index, item, "shopping_list_id"),
                _item_string(action, index, item, "note"),
                item.get("quantity"),
                item.get("food_id"),
                item.get("unit_id"),
                item.get("label_id"),
            )
        )
    response = create_many_api_households_shopping_items_create_bulk_post.sync_detailed(
        client=client, body=bodies
    )
    return expect_dict(action, response, HTTPStatus.CREATED)


def update_shopping_list_item(
    client: AuthenticatedClient,
    item_id: str,
    *,
    note: str | None = None,
    quantity: float | None = None,
    checked: bool | None = None,
    label_id: str | None = None,
) -> dict[str, Any]:
    """Update a shopping list item. Returns the updated item payload.

    The endpoint PUT-replaces the item, and the body model defaults most fields
    to concrete values rather than leaving them unset. The current item is
    therefore fetched and the body rebuilt from it, so unsupplied fields and the
    item's food and unit links keep their current values; only the caller's
    edits are applied on top. Recipe links are the exception: Mealie drops an
    item's recipe references server-side when the update checks it off,
    regardless of the merged body.
    """
    require_non_empty("item_id", item_id)
    if note is None and quantity is None and checked is None and label_id is None:
        raise ToolError("update_shopping_list_item requires at least one field to update")

    fetched = get_one_api_households_shopping_items_item_id_get.sync_detailed(
        item_id, client=client
    )
    current = expect_dict("update_shopping_list_item", fetched)
    body = ShoppingListItemUpdate.from_dict(current)
    body.additional_properties = {}
    _apply_item_edits(body, note=note, quantity=quantity, checked=checked, label_id=label_id)
    response = update_one_api_households_shopping_items_item_id_put.sync_detailed(
        item_id, client=client, body=body
    )
    if response.status_code != HTTPStatus.OK:
        raise_api_error("update_shopping_list_item", int(response.status_code), response.content)
    return _single_item("update_shopping_list_item", response, ("updatedItems",))


def update_shopping_list_items(
    client: AuthenticatedClient, items: list[dict[str, Any]]
) -> dict[str, Any]:
    """Update several shopping list items in one call. Returns the collection envelope.

    The endpoint PUT-replaces every item in the body, so each item is fetched
    first and its body rebuilt from the current state with the caller's edits
    applied on top. Every item is validated before the first fetch, so a
    malformed entry raises before any request is sent.
    """
    action = "update_shopping_list_items"
    if not items:
        raise ToolError("items must contain at least one item")

    edits: list[tuple[str, dict[str, Any]]] = []
    for index, item in enumerate(items):
        _require_item_fields(action, index, item, UPDATE_ITEM_FIELDS)
        item_id = _item_string(action, index, item, "id")
        fields = {key: value for key, value in item.items() if key != "id" and value is not None}
        if not fields:
            raise ToolError(f"{action} items[{index}] requires at least one field to update")
        edits.append((item_id, fields))

    bodies = []
    for item_id, fields in edits:
        fetched = get_one_api_households_shopping_items_item_id_get.sync_detailed(
            item_id, client=client
        )
        current = expect_dict(action, fetched)
        body = ShoppingListItemUpdateBulk.from_dict(current)
        body.additional_properties = {}
        _apply_item_edits(body, **fields)
        bodies.append(body)

    response = update_many_api_households_shopping_items_put.sync_detailed(
        client=client, body=bodies
    )
    return expect_dict(action, response)


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
        food_id: str | None = None,
        unit_id: str | None = None,
        label_id: str | None = None,
    ) -> dict[str, Any]:
        """Add an item to a shopping list.

        The item is described by ``note`` (the text shown on the list), with an
        optional ``quantity``. Giving ``food_id`` and ``unit_id`` makes Mealie
        aggregate: an item whose food and unit match an unchecked item already
        on the list is merged into it and their quantities are summed, so the
        returned item is the merged one and no new line appears. A checked item
        does not absorb the new one. Without a food and a unit the item is free
        text and always adds a line of its own. Recipe associations are not set
        through this tool.

        Args:
            shopping_list_id: UUID of the shopping list to add to.
            note: Free-text description of the item. Required.
            quantity: Optional amount. Defaults to 1 in Mealie when omitted.
            food_id: UUID of the food to link, from ``mealie_list_foods``. A
                food name is not accepted.
            unit_id: UUID of the unit to link, from ``mealie_list_units``. A
                unit name is not accepted.
            label_id: UUID of the multi-purpose label that sorts the item into
                an aisle, from ``mealie_list_labels``. A label name is not
                accepted. Labels the item itself, independent of the label its
                food carries.

        Returns:
            The created shopping list item as a JSON-compatible dict, or the
            item it was merged into.
        """
        return add_shopping_list_item(
            get_client(),
            shopping_list_id=shopping_list_id,
            note=note,
            quantity=quantity,
            food_id=food_id,
            unit_id=unit_id,
            label_id=label_id,
        )

    @mcp.tool(name="mealie_add_shopping_list_items")
    def _add_shopping_list_items(items: list[dict[str, Any]]) -> dict[str, Any]:
        """Create several shopping list items in one call.

        One request instead of one per item. Each item names its own target
        list, so a single call can fill several lists. Aggregation applies as in
        ``mealie_add_shopping_list_item``: items sharing a food and a unit with
        an unchecked existing item, or with each other, are merged, so fewer
        items can come back than were sent. The write is not atomic; if one item
        fails, the items before it are already created.

        Args:
            items: Item objects, at least one. Each takes
                ``shopping_list_id`` (UUID, required), ``note`` (required),
                ``quantity``, ``food_id``, ``unit_id`` and ``label_id``, with
                the same meaning as in ``mealie_add_shopping_list_item``. Any
                other field is rejected.

        Returns:
            A collection envelope with ``createdItems``, ``updatedItems`` and
            ``deletedItems``. An item merged into an existing one appears under
            ``updatedItems``, not ``createdItems``.
        """
        return add_shopping_list_items(get_client(), items=items)

    @mcp.tool(name="mealie_update_shopping_list_item")
    def _update_shopping_list_item(
        item_id: str,
        note: str | None = None,
        quantity: float | None = None,
        checked: bool | None = None,
        label_id: str | None = None,
    ) -> dict[str, Any]:
        """Edit a shopping list item, or check it off.

        Only the fields supplied change; omitted fields keep their current value
        and the item's food and unit links are preserved. Checking an item off
        additionally drops its recipe links, which Mealie clears server-side. At
        least one of ``note``, ``quantity``, ``checked``, or ``label_id`` must be
        provided.

        Args:
            item_id: UUID of the shopping list item.
            note: New free-text description.
            quantity: New amount.
            checked: ``True`` to mark the item bought, ``False`` to uncheck it.
            label_id: UUID of the multi-purpose label that sorts the item into
                an aisle, from ``mealie_list_labels``. A label name is not
                accepted. Pass an empty string to detach the current label.

        Returns:
            The updated shopping list item as a JSON-compatible dict.
        """
        return update_shopping_list_item(
            get_client(),
            item_id=item_id,
            note=note,
            quantity=quantity,
            checked=checked,
            label_id=label_id,
        )

    @mcp.tool(name="mealie_update_shopping_list_items")
    def _update_shopping_list_items(items: list[dict[str, Any]]) -> dict[str, Any]:
        """Edit several shopping list items in one call, or check them off.

        One request instead of one per item. Each item is identified by its own
        ``id``, so a single call can span several lists. Only the fields
        supplied on an item change; its other fields, including its food, unit,
        and recipe links, keep their current values. Every item is read before
        anything is written, so an id matching no item fails the call and leaves
        the other items unchanged. Unchecking an item whose food and unit match
        another unchecked item merges the two: the survivor comes back under
        ``updatedItems`` and the absorbed one under ``deletedItems``.

        Args:
            items: Item objects, at least one. Each takes ``id`` (UUID of the
                item, required) plus at least one of ``note``, ``quantity``,
                ``checked`` and ``label_id``, with the same meaning as in
                ``mealie_update_shopping_list_item``. Any other field is
                rejected.

        Returns:
            A collection envelope with ``createdItems``, ``updatedItems`` and
            ``deletedItems``.
        """
        return update_shopping_list_items(get_client(), items=items)

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
