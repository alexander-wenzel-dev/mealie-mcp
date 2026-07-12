"""Multi purpose label tools.

Mirrors `mealie_mcp.client.api.groups_multi_purpose_labels`. Exposes CRUD for the
group's multi purpose labels, the categories that shopping list items and foods
carry through their ``labelId``. Assigning a label to a food or a shopping list
item is out of scope here; it belongs to those resources' own tools. ``color`` is
an opaque hex string passed through verbatim, with hex validation left to Mealie.
"""

from __future__ import annotations

from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.groups_multi_purpose_labels import (
    create_one_api_groups_labels_post,
    delete_one_api_groups_labels_item_id_delete,
    get_all_api_groups_labels_get,
    get_one_api_groups_labels_item_id_get,
    update_one_api_groups_labels_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.multi_purpose_label_create import MultiPurposeLabelCreate
from mealie_mcp.client.models.multi_purpose_label_update import MultiPurposeLabelUpdate
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_non_empty,
    require_pagination,
    to_unset,
)


def list_labels(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List the group's multi purpose labels, paginated. Returns the envelope."""
    require_pagination(page, per_page)
    response = get_all_api_groups_labels_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_labels", response)


def create_label(
    client: AuthenticatedClient,
    name: str,
    color: str | None = None,
) -> dict[str, Any]:
    """Create a label. Returns the new label payload.

    ``color`` is an opaque hex string (e.g. ``"#RRGGBB"``) stored verbatim.
    Mealie defaults it to ``#959595`` when omitted and validates the format.
    """
    require_non_empty("name", name)
    body = MultiPurposeLabelCreate(name=name, color=to_unset(color))
    response = create_one_api_groups_labels_post.sync_detailed(client=client, body=body)
    return expect_dict("create_label", response)


def get_label(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a label by id. Returns the label payload."""
    require_non_empty("item_id", item_id)
    response = get_one_api_groups_labels_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_label", response)


def update_label(
    client: AuthenticatedClient,
    item_id: str,
    name: str | None = None,
    color: str | None = None,
) -> dict[str, Any]:
    """Edit a label's name or color. Returns the updated payload.

    Mealie's PUT replaces the resource rather than patching it, so a field absent
    from the request body resets to its schema default. The current label is
    fetched and the caller's edits are merged over it, so the field left unset
    survives the replace. The prefetch is routed through
    ``expect_dict("update_label", ...)`` so any failure surfaces under the
    caller's tool name.
    """
    require_non_empty("item_id", item_id)
    if name is None and color is None:
        raise ToolError("update_label requires at least one field to update")
    if name is not None:
        require_non_empty("name", name)

    prefetch = get_one_api_groups_labels_item_id_get.sync_detailed(item_id, client=client)
    existing = expect_dict("update_label", prefetch)
    body = MultiPurposeLabelUpdate.from_dict(existing)
    body.additional_properties = {}
    if name is not None:
        body.name = name
    if color is not None:
        body.color = color

    response = update_one_api_groups_labels_item_id_put.sync_detailed(
        item_id, client=client, body=body
    )
    return expect_dict("update_label", response)


def delete_label(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a label by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)
    response = delete_one_api_groups_labels_item_id_delete.sync_detailed(item_id, client=client)
    return ack_delete("delete_label", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the multi purpose label tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_labels")
    def _list_labels(
        page: int = 1,
        per_page: int = 50,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List the group's multi purpose labels, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            order_by: Optional column name to sort on (e.g. ``"name"``).
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_labels(
            get_client(),
            page=page,
            per_page=per_page,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_create_label")
    def _create_label(name: str, color: str | None = None) -> dict[str, Any]:
        """Create a multi purpose label.

        Labels categorize shopping list items and foods. Assigning a label to
        one of those is done through their own tools, not here.

        Args:
            name: Display name for the label. Required, must be non-empty.
            color: Optional hex color string such as ``"#RRGGBB"``. Stored
                verbatim and validated by Mealie; defaults to ``#959595``.

        Returns:
            The newly created label payload as a JSON-compatible dict.
        """
        return create_label(get_client(), name=name, color=color)

    @mcp.tool(name="mealie_get_label")
    def _get_label(item_id: str) -> dict[str, Any]:
        """Fetch a single multi purpose label by id.

        Args:
            item_id: UUID of the label.

        Returns:
            The label payload as a JSON-compatible dict.
        """
        return get_label(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_update_label")
    def _update_label(
        item_id: str,
        name: str | None = None,
        color: str | None = None,
    ) -> dict[str, Any]:
        """Edit an existing multi purpose label.

        Only the supplied fields change; a field left unset is preserved.

        Args:
            item_id: UUID of the label to update.
            name: Optional new display name.
            color: Optional new hex color string such as ``"#RRGGBB"``.

        Returns:
            The updated label payload as a JSON-compatible dict.
        """
        return update_label(get_client(), item_id=item_id, name=name, color=color)

    @mcp.tool(name="mealie_delete_label")
    def _delete_label(item_id: str) -> dict[str, Any]:
        """Delete a multi purpose label from Mealie by id.

        Args:
            item_id: UUID of the label to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_label(get_client(), item_id=item_id)
