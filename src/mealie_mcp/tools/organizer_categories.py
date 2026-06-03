"""Recipe category tools.

Mirrors `mealie_mcp.client.api.organizer_categories`. Exposes list, read,
create, update, and delete for recipe categories.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP

from mealie_mcp.client.api.organizer_categories import (
    create_one_api_organizers_categories_post,
    delete_one_api_organizers_categories_item_id_delete,
    get_all_api_organizers_categories_get,
    get_one_api_organizers_categories_item_id_get,
    update_one_api_organizers_categories_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.category_in import CategoryIn
from mealie_mcp.client.models.order_direction import OrderDirection
from mealie_mcp.client.types import UNSET, Unset
from mealie_mcp.client_factory import build_client
from mealie_mcp.tools._common import expect_dict, raise_api_error, require_non_empty


def list_categories(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List recipe categories, paginated. Returns the pagination envelope."""
    direction: OrderDirection | Unset = UNSET
    if order_direction is not None:
        direction = OrderDirection(order_direction)

    response = get_all_api_organizers_categories_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=search if search is not None else UNSET,
        order_by=order_by if order_by is not None else UNSET,
        order_direction=direction,
    )
    return expect_dict("list_categories", response)


def get_category(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a category by id. Returns the category payload."""
    require_non_empty("item_id", item_id)

    response = get_one_api_organizers_categories_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_category", response)


def create_category(client: AuthenticatedClient, name: str) -> dict[str, Any]:
    """Create a category with the given name. Returns the new category payload."""
    require_non_empty("name", name)

    response = create_one_api_organizers_categories_post.sync_detailed(
        client=client, body=CategoryIn(name=name)
    )
    return expect_dict("create_category", response, HTTPStatus.CREATED)


def update_category(client: AuthenticatedClient, item_id: str, name: str) -> dict[str, Any]:
    """Rename an existing category. Returns the updated category payload."""
    require_non_empty("item_id", item_id)
    require_non_empty("name", name)

    response = update_one_api_organizers_categories_item_id_put.sync_detailed(
        item_id, client=client, body=CategoryIn(name=name)
    )
    return expect_dict("update_category", response)


def delete_category(client: AuthenticatedClient, item_id: str) -> dict[str, str]:
    """Delete a category by id. Returns ``{"id": item_id}`` on success."""
    require_non_empty("item_id", item_id)

    response = delete_one_api_organizers_categories_item_id_delete.sync_detailed(
        item_id, client=client
    )
    if response.status_code != HTTPStatus.OK:
        raise_api_error("delete_category", int(response.status_code), response.content)
    return {"id": item_id}


def register(mcp: FastMCP) -> None:
    """Register the category tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_categories")
    def _list_categories(
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List recipe categories from Mealie, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50.
            search: Optional free-text search.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_categories(
            build_client(),
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_get_category")
    def _get_category(item_id: str) -> dict[str, Any]:
        """Fetch a single category from Mealie by id.

        Args:
            item_id: UUID of the category.

        Returns:
            The category payload as a JSON-compatible dict.
        """
        return get_category(build_client(), item_id=item_id)

    @mcp.tool(name="mealie_create_category")
    def _create_category(name: str) -> dict[str, Any]:
        """Create a recipe category in Mealie.

        Args:
            name: Human readable category name. Required, must be non-empty.

        Returns:
            The newly created category payload as a JSON-compatible dict.
        """
        return create_category(build_client(), name=name)

    @mcp.tool(name="mealie_update_category")
    def _update_category(item_id: str, name: str) -> dict[str, Any]:
        """Rename an existing category in Mealie.

        Args:
            item_id: UUID of the category to update.
            name: New name. Required, must be non-empty.

        Returns:
            The updated category payload as a JSON-compatible dict.
        """
        return update_category(build_client(), item_id=item_id, name=name)

    @mcp.tool(name="mealie_delete_category")
    def _delete_category(item_id: str) -> dict[str, str]:
        """Delete a category from Mealie by id.

        Args:
            item_id: UUID of the category to delete.

        Returns:
            ``{"id": <item_id>}`` confirming the delete.
        """
        return delete_category(build_client(), item_id=item_id)
