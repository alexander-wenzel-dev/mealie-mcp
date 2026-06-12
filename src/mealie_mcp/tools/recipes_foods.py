"""Recipe food tools.

Mirrors `mealie_mcp.client.api.recipes_foods`. Exposes list, read, create,
update, and delete for ingredient foods.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP

from mealie_mcp.client.api.recipes_foods import (
    create_one_api_foods_post,
    delete_one_api_foods_item_id_delete,
    get_all_api_foods_get,
    get_one_api_foods_item_id_get,
    update_one_api_foods_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_food import CreateIngredientFood
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_non_empty,
    require_per_page,
    to_unset,
)


def list_foods(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List ingredient foods, paginated. Returns the pagination envelope."""
    require_per_page(per_page)
    response = get_all_api_foods_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=to_unset(search),
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_foods", response)


def get_food(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a food by id. Returns the food payload."""
    require_non_empty("item_id", item_id)

    response = get_one_api_foods_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_food", response)


def create_food(client: AuthenticatedClient, name: str) -> dict[str, Any]:
    """Create a food with the given name. Returns the new food payload."""
    require_non_empty("name", name)

    response = create_one_api_foods_post.sync_detailed(
        client=client, body=CreateIngredientFood(name=name)
    )
    return expect_dict("create_food", response, HTTPStatus.CREATED)


def update_food(client: AuthenticatedClient, item_id: str, name: str) -> dict[str, Any]:
    """Rename an existing food. Returns the updated food payload.

    Mealie's PUT replaces the resource rather than patching it, so fields
    absent from the request body reset to their schema defaults. The current
    food is fetched and the merged payload is sent so untouched fields are
    preserved. The prefetch is routed through ``expect_dict("update_food", ...)``
    so any failure surfaces under the caller's tool name.
    """
    require_non_empty("item_id", item_id)
    require_non_empty("name", name)

    prefetch = get_one_api_foods_item_id_get.sync_detailed(item_id, client=client)
    existing = expect_dict("update_food", prefetch)
    body = CreateIngredientFood.from_dict(existing)
    body.additional_properties = {}
    body.name = name

    response = update_one_api_foods_item_id_put.sync_detailed(item_id, client=client, body=body)
    return expect_dict("update_food", response)


def delete_food(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a food by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)

    response = delete_one_api_foods_item_id_delete.sync_detailed(item_id, client=client)
    return ack_delete("delete_food", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the food tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_foods")
    def _list_foods(
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List ingredient foods from Mealie, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50. Capped at 100.
            search: Optional free-text search.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_foods(
            get_client(),
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_get_food")
    def _get_food(item_id: str) -> dict[str, Any]:
        """Fetch a single food from Mealie by id.

        Args:
            item_id: UUID of the food.

        Returns:
            The food payload as a JSON-compatible dict.
        """
        return get_food(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_create_food")
    def _create_food(name: str) -> dict[str, Any]:
        """Create an ingredient food in Mealie.

        Args:
            name: Human readable food name. Required, must be non-empty.

        Returns:
            The newly created food payload as a JSON-compatible dict.
        """
        return create_food(get_client(), name=name)

    @mcp.tool(name="mealie_update_food")
    def _update_food(item_id: str, name: str) -> dict[str, Any]:
        """Rename an existing food in Mealie.

        Args:
            item_id: UUID of the food to update.
            name: New name. Required, must be non-empty.

        Returns:
            The updated food payload as a JSON-compatible dict.
        """
        return update_food(get_client(), item_id=item_id, name=name)

    @mcp.tool(name="mealie_delete_food")
    def _delete_food(item_id: str) -> dict[str, Any]:
        """Delete a food from Mealie by id.

        Args:
            item_id: UUID of the food to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_food(get_client(), item_id=item_id)
