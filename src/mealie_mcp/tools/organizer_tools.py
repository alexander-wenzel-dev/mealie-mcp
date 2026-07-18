"""Recipe tool (equipment) tools.

Mirrors `mealie_mcp.client.api.organizer_tools`. Exposes list, read, create,
update, and delete for recipe tools, the kitchen equipment a recipe calls for.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP

from mealie_mcp.client.api.organizer_tools import (
    create_one_api_organizers_tools_post,
    delete_one_api_organizers_tools_item_id_delete,
    get_all_api_organizers_tools_get,
    get_one_api_organizers_tools_item_id_get,
    get_one_by_slug_api_organizers_tools_slug_tool_slug_get,
    update_one_api_organizers_tools_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.recipe_tool_create import RecipeToolCreate
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_non_empty,
    require_pagination,
    to_unset,
)


def list_tools(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List recipe tools, paginated. Returns the pagination envelope."""
    require_pagination(page, per_page)
    response = get_all_api_organizers_tools_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=to_unset(search),
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_tools", response)


def get_tool(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a tool by id. Returns the tool payload."""
    require_non_empty("item_id", item_id)

    response = get_one_api_organizers_tools_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_tool", response)


def get_tool_by_slug(client: AuthenticatedClient, slug: str) -> dict[str, Any]:
    """Fetch a tool by slug. Returns the tool payload."""
    require_non_empty("slug", slug)

    response = get_one_by_slug_api_organizers_tools_slug_tool_slug_get.sync_detailed(
        slug, client=client
    )
    return expect_dict("get_tool_by_slug", response)


def create_tool(client: AuthenticatedClient, name: str) -> dict[str, Any]:
    """Create a tool with the given name. Returns the new tool payload."""
    require_non_empty("name", name)

    response = create_one_api_organizers_tools_post.sync_detailed(
        client=client, body=RecipeToolCreate(name=name)
    )
    return expect_dict("create_tool", response, HTTPStatus.CREATED)


def update_tool(client: AuthenticatedClient, item_id: str, name: str) -> dict[str, Any]:
    """Rename an existing tool. Returns the updated tool payload.

    Mealie's PUT replaces the resource rather than patching it, so fields
    absent from the request body reset to their schema defaults. The current
    tool is fetched and the merged payload is sent so untouched fields are
    preserved. The prefetch is routed through ``expect_dict("update_tool", ...)``
    so any failure surfaces under the caller's tool name.
    """
    require_non_empty("item_id", item_id)
    require_non_empty("name", name)

    prefetch = get_one_api_organizers_tools_item_id_get.sync_detailed(item_id, client=client)
    existing = expect_dict("update_tool", prefetch)
    body = RecipeToolCreate.from_dict(existing)
    body.additional_properties = {}
    body.name = name

    response = update_one_api_organizers_tools_item_id_put.sync_detailed(
        item_id, client=client, body=body
    )
    return expect_dict("update_tool", response)


def delete_tool(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a tool by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)

    response = delete_one_api_organizers_tools_item_id_delete.sync_detailed(item_id, client=client)
    return ack_delete("delete_tool", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the tool (equipment) tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_tools")
    def _list_tools(
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List recipe tools (kitchen equipment) from Mealie, paginated.

        Use this to find a tool slug. The recipe list filter and the by-slug
        read tool match tools by slug, not display name, and a display name
        returns no matches.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            search: Optional free-text search.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_tools(
            get_client(),
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_get_tool")
    def _get_tool(item_id: str) -> dict[str, Any]:
        """Fetch a single tool from Mealie by id.

        Returns a compact payload without the ``recipes`` list. Use
        ``mealie_get_tool_by_slug`` to read the recipes using the tool.

        Args:
            item_id: UUID of the tool.

        Returns:
            The tool payload as a JSON-compatible dict, without ``recipes``.
        """
        return get_tool(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_get_tool_by_slug")
    def _get_tool_by_slug(slug: str) -> dict[str, Any]:
        """Fetch a single tool from Mealie by slug.

        Useful when you have a tool slug from ``mealie_list_recipes`` results
        and need the underlying record (for example to find its id).

        Args:
            slug: The tool slug.

        Returns:
            The tool payload as a JSON-compatible dict.
        """
        return get_tool_by_slug(get_client(), slug=slug)

    @mcp.tool(name="mealie_create_tool")
    def _create_tool(name: str) -> dict[str, Any]:
        """Create a recipe tool (kitchen equipment) in Mealie.

        Args:
            name: Human readable tool name. Required, must be non-empty.

        Returns:
            The newly created tool payload as a JSON-compatible dict.
        """
        return create_tool(get_client(), name=name)

    @mcp.tool(name="mealie_update_tool")
    def _update_tool(item_id: str, name: str) -> dict[str, Any]:
        """Rename an existing tool in Mealie.

        Args:
            item_id: UUID of the tool to update.
            name: New name. Required, must be non-empty.

        Returns:
            The updated tool payload as a JSON-compatible dict.
        """
        return update_tool(get_client(), item_id=item_id, name=name)

    @mcp.tool(name="mealie_delete_tool")
    def _delete_tool(item_id: str) -> dict[str, Any]:
        """Delete a tool from Mealie by id.

        Args:
            item_id: UUID of the tool to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_tool(get_client(), item_id=item_id)
