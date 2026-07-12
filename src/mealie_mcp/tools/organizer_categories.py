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
    get_all_empty_api_organizers_categories_empty_get,
    get_one_api_organizers_categories_item_id_get,
    get_one_by_slug_api_organizers_categories_slug_category_slug_get,
    update_one_api_organizers_categories_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.category_in import CategoryIn
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    expect_list,
    parse_order_direction,
    require_non_empty,
    require_pagination,
    to_unset,
)


def list_categories(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List recipe categories, paginated. Returns the pagination envelope."""
    require_pagination(page, per_page)
    response = get_all_api_organizers_categories_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=to_unset(search),
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_categories", response)


def list_empty_categories(client: AuthenticatedClient) -> list[Any]:
    """List categories with no recipes assigned. Returns a bare list."""
    response = get_all_empty_api_organizers_categories_empty_get.sync_detailed(client=client)
    return expect_list("list_empty_categories", response)


def get_category(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a category by id. Returns the category payload."""
    require_non_empty("item_id", item_id)

    response = get_one_api_organizers_categories_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_category", response)


def get_category_by_slug(client: AuthenticatedClient, slug: str) -> dict[str, Any]:
    """Fetch a category by slug. Returns the category payload."""
    require_non_empty("slug", slug)

    response = get_one_by_slug_api_organizers_categories_slug_category_slug_get.sync_detailed(
        slug, client=client
    )
    return expect_dict("get_category_by_slug", response)


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


def delete_category(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a category by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)

    response = delete_one_api_organizers_categories_item_id_delete.sync_detailed(
        item_id, client=client
    )
    return ack_delete("delete_category", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
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

        Use this to find a category slug. The recipe list filter and the
        by-slug read tool match categories by slug, not display name, and a
        display name returns no matches.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            search: Optional free-text search.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_categories(
            get_client(),
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_list_empty_categories")
    def _list_empty_categories() -> list[Any]:
        """List recipe categories that have no recipes assigned.

        Use this to find unused categories worth cleaning up. Delete one with
        ``mealie_delete_category``. Takes no arguments and returns every empty
        category at once, not a page.

        Returns:
            A bare list of category payloads, each with no recipes assigned.
            Empty when every category is in use.
        """
        return list_empty_categories(get_client())

    @mcp.tool(name="mealie_get_category")
    def _get_category(item_id: str) -> dict[str, Any]:
        """Fetch a single category from Mealie by id.

        Args:
            item_id: UUID of the category.

        Returns:
            The category payload as a JSON-compatible dict.
        """
        return get_category(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_get_category_by_slug")
    def _get_category_by_slug(slug: str) -> dict[str, Any]:
        """Fetch a single category from Mealie by slug.

        Useful when you have a category slug from ``mealie_list_recipes``
        results and need the underlying record (for example to find its id).

        Args:
            slug: The category slug.

        Returns:
            The category payload as a JSON-compatible dict.
        """
        return get_category_by_slug(get_client(), slug=slug)

    @mcp.tool(name="mealie_create_category")
    def _create_category(name: str) -> dict[str, Any]:
        """Create a recipe category in Mealie.

        Args:
            name: Human readable category name. Required, must be non-empty.

        Returns:
            The newly created category payload as a JSON-compatible dict.
        """
        return create_category(get_client(), name=name)

    @mcp.tool(name="mealie_update_category")
    def _update_category(item_id: str, name: str) -> dict[str, Any]:
        """Rename an existing category in Mealie.

        Args:
            item_id: UUID of the category to update.
            name: New name. Required, must be non-empty.

        Returns:
            The updated category payload as a JSON-compatible dict.
        """
        return update_category(get_client(), item_id=item_id, name=name)

    @mcp.tool(name="mealie_delete_category")
    def _delete_category(item_id: str) -> dict[str, Any]:
        """Delete a category from Mealie by id.

        Args:
            item_id: UUID of the category to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_category(get_client(), item_id=item_id)
