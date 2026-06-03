"""Recipe tag tools.

Mirrors `mealie_mcp.client.api.organizer_tags`. Exposes list, read, create,
update, and delete for recipe tags.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP

from mealie_mcp.client.api.organizer_tags import (
    create_one_api_organizers_tags_post,
    delete_recipe_tag_api_organizers_tags_item_id_delete,
    get_all_api_organizers_tags_get,
    get_one_api_organizers_tags_item_id_get,
    update_one_api_organizers_tags_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.order_direction import OrderDirection
from mealie_mcp.client.models.tag_in import TagIn
from mealie_mcp.client.types import UNSET, Unset
from mealie_mcp.client_factory import build_client
from mealie_mcp.tools._common import expect_dict, raise_api_error, require_non_empty


def list_tags(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List recipe tags, paginated. Returns the pagination envelope."""
    direction: OrderDirection | Unset = UNSET
    if order_direction is not None:
        direction = OrderDirection(order_direction)

    response = get_all_api_organizers_tags_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=search if search is not None else UNSET,
        order_by=order_by if order_by is not None else UNSET,
        order_direction=direction,
    )
    return expect_dict("list_tags", response)


def get_tag(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a tag by id. Returns the tag payload."""
    require_non_empty("item_id", item_id)

    response = get_one_api_organizers_tags_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_tag", response)


def create_tag(client: AuthenticatedClient, name: str) -> dict[str, Any]:
    """Create a tag with the given name. Returns the new tag payload."""
    require_non_empty("name", name)

    response = create_one_api_organizers_tags_post.sync_detailed(
        client=client, body=TagIn(name=name)
    )
    return expect_dict("create_tag", response, HTTPStatus.CREATED)


def update_tag(client: AuthenticatedClient, item_id: str, name: str) -> dict[str, Any]:
    """Rename an existing tag. Returns the updated tag payload."""
    require_non_empty("item_id", item_id)
    require_non_empty("name", name)

    response = update_one_api_organizers_tags_item_id_put.sync_detailed(
        item_id, client=client, body=TagIn(name=name)
    )
    return expect_dict("update_tag", response)


def delete_tag(client: AuthenticatedClient, item_id: str) -> dict[str, str]:
    """Delete a tag by id. Returns ``{"id": item_id}`` on success."""
    require_non_empty("item_id", item_id)

    response = delete_recipe_tag_api_organizers_tags_item_id_delete.sync_detailed(
        item_id, client=client
    )
    if response.status_code != HTTPStatus.OK:
        raise_api_error("delete_tag", int(response.status_code), response.content)
    return {"id": item_id}


def register(mcp: FastMCP) -> None:
    """Register the tag tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_tags")
    def _list_tags(
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List recipe tags from Mealie, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50.
            search: Optional free-text search.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_tags(
            build_client(),
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_get_tag")
    def _get_tag(item_id: str) -> dict[str, Any]:
        """Fetch a single tag from Mealie by id.

        Args:
            item_id: UUID of the tag.

        Returns:
            The tag payload as a JSON-compatible dict.
        """
        return get_tag(build_client(), item_id=item_id)

    @mcp.tool(name="mealie_create_tag")
    def _create_tag(name: str) -> dict[str, Any]:
        """Create a recipe tag in Mealie.

        Args:
            name: Human readable tag name. Required, must be non-empty.

        Returns:
            The newly created tag payload as a JSON-compatible dict.
        """
        return create_tag(build_client(), name=name)

    @mcp.tool(name="mealie_update_tag")
    def _update_tag(item_id: str, name: str) -> dict[str, Any]:
        """Rename an existing tag in Mealie.

        Args:
            item_id: UUID of the tag to update.
            name: New name. Required, must be non-empty.

        Returns:
            The updated tag payload as a JSON-compatible dict.
        """
        return update_tag(build_client(), item_id=item_id, name=name)

    @mcp.tool(name="mealie_delete_tag")
    def _delete_tag(item_id: str) -> dict[str, str]:
        """Delete a tag from Mealie by id.

        Args:
            item_id: UUID of the tag to delete.

        Returns:
            ``{"id": <item_id>}`` confirming the delete.
        """
        return delete_tag(build_client(), item_id=item_id)
