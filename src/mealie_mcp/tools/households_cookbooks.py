"""Household cookbook tools.

Mirrors `mealie_mcp.client.api.households_cookbooks`. Exposes CRUD for cookbooks,
the filter-based recipe collections that `mealie_list_recipes` reads through its
`cookbook` argument. A cookbook stores an opaque Mealie filter DSL in
`queryFilterString`; the create and update tools pass it straight through rather
than building it from structured category, tag, or tool inputs. Listing the
recipes a cookbook resolves to is out of scope; pass the cookbook to
`mealie_list_recipes`.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_cookbooks import (
    create_one_api_households_cookbooks_post,
    delete_one_api_households_cookbooks_item_id_delete,
    get_all_api_households_cookbooks_get,
    get_one_api_households_cookbooks_item_id_get,
    update_one_api_households_cookbooks_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_cook_book import CreateCookBook
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_non_empty,
    require_per_page,
    to_unset,
)


def list_cookbooks(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List the household's cookbooks, paginated. Returns the pagination envelope."""
    require_per_page(per_page)
    response = get_all_api_households_cookbooks_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_cookbooks", response)


def create_cookbook(
    client: AuthenticatedClient,
    name: str,
    description: str | None = None,
    query_filter_string: str | None = None,
) -> dict[str, Any]:
    """Create a cookbook. Returns the new cookbook payload.

    ``query_filter_string`` is the opaque Mealie filter DSL that selects which
    recipes the cookbook resolves to. It is stored verbatim and parsed
    server-side.
    """
    require_non_empty("name", name)
    body = CreateCookBook(
        name=name,
        description=to_unset(description),
        query_filter_string=to_unset(query_filter_string),
    )
    response = create_one_api_households_cookbooks_post.sync_detailed(client=client, body=body)
    return expect_dict("create_cookbook", response, HTTPStatus.CREATED)


def get_cookbook(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a cookbook by id. Returns the cookbook payload."""
    require_non_empty("item_id", item_id)
    response = get_one_api_households_cookbooks_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_cookbook", response)


def update_cookbook(
    client: AuthenticatedClient,
    item_id: str,
    name: str | None = None,
    description: str | None = None,
    query_filter_string: str | None = None,
) -> dict[str, Any]:
    """Edit a cookbook's name, description, or filter. Returns the updated payload.

    Mealie's PUT replaces the resource rather than patching it, so fields absent
    from the request body reset to their schema defaults. The current cookbook is
    fetched and the merged payload is sent so ``slug``, ``position``, and
    ``public`` survive untouched. The prefetch is routed through
    ``expect_dict("update_cookbook", ...)`` so any failure surfaces under the
    caller's tool name.
    """
    require_non_empty("item_id", item_id)
    if name is None and description is None and query_filter_string is None:
        raise ToolError("update_cookbook requires at least one field to update")
    if name is not None:
        require_non_empty("name", name)

    prefetch = get_one_api_households_cookbooks_item_id_get.sync_detailed(item_id, client=client)
    existing = expect_dict("update_cookbook", prefetch)
    body = CreateCookBook.from_dict(existing)
    body.additional_properties = {}
    if name is not None:
        body.name = name
    if description is not None:
        body.description = description
    if query_filter_string is not None:
        body.query_filter_string = query_filter_string

    response = update_one_api_households_cookbooks_item_id_put.sync_detailed(
        item_id, client=client, body=body
    )
    return expect_dict("update_cookbook", response)


def delete_cookbook(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a cookbook by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)
    response = delete_one_api_households_cookbooks_item_id_delete.sync_detailed(
        item_id, client=client
    )
    return ack_delete("delete_cookbook", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the household cookbook tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_cookbooks")
    def _list_cookbooks(
        page: int = 1,
        per_page: int = 50,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List the household's cookbooks, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50. Capped at 100.
            order_by: Optional column name to sort on (e.g. ``"name"``).
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_cookbooks(
            get_client(),
            page=page,
            per_page=per_page,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_create_cookbook")
    def _create_cookbook(
        name: str,
        description: str | None = None,
        query_filter_string: str | None = None,
    ) -> dict[str, Any]:
        """Create a cookbook, a filter-based recipe collection.

        Args:
            name: Display name for the cookbook. Required.
            description: Optional free-text description.
            query_filter_string: Optional Mealie filter DSL that selects which
                recipes the cookbook resolves to (e.g.
                ``'recipe_category.name CONTAINS ALL ["Dinner"]'``). Stored
                verbatim and parsed server-side. Pass the cookbook to
                ``mealie_list_recipes`` to read the recipes it resolves.

        Returns:
            The newly created cookbook payload as a JSON-compatible dict.
        """
        return create_cookbook(
            get_client(),
            name=name,
            description=description,
            query_filter_string=query_filter_string,
        )

    @mcp.tool(name="mealie_get_cookbook")
    def _get_cookbook(item_id: str) -> dict[str, Any]:
        """Fetch a single cookbook by id.

        Args:
            item_id: UUID of the cookbook.

        Returns:
            The cookbook payload as a JSON-compatible dict.
        """
        return get_cookbook(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_update_cookbook")
    def _update_cookbook(
        item_id: str,
        name: str | None = None,
        description: str | None = None,
        query_filter_string: str | None = None,
    ) -> dict[str, Any]:
        """Edit an existing cookbook.

        Only the supplied fields change; ``slug``, ``position``, ``public``, and
        any field left unset are preserved.

        Args:
            item_id: UUID of the cookbook to update.
            name: Optional new display name.
            description: Optional new description.
            query_filter_string: Optional new Mealie filter DSL.

        Returns:
            The updated cookbook payload as a JSON-compatible dict.
        """
        return update_cookbook(
            get_client(),
            item_id=item_id,
            name=name,
            description=description,
            query_filter_string=query_filter_string,
        )

    @mcp.tool(name="mealie_delete_cookbook")
    def _delete_cookbook(item_id: str) -> dict[str, Any]:
        """Delete a cookbook from Mealie by id.

        Args:
            item_id: UUID of the cookbook to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_cookbook(get_client(), item_id=item_id)
