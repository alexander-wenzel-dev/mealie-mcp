"""Recipe comment tools.

Mirrors `mealie_mcp.client.api.recipe_comments`. Exposes create, read, list,
update, and delete for comments, plus the recipe-scoped listing.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from fastmcp import FastMCP

from mealie_mcp.client.api.recipe_comments import (
    create_one_api_comments_post,
    delete_one_api_comments_item_id_delete,
    get_all_api_comments_get,
    get_one_api_comments_item_id_get,
    get_recipe_comments_api_recipes_slug_comments_get,
    update_one_api_comments_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.recipe_comment_create import RecipeCommentCreate
from mealie_mcp.client.models.recipe_comment_update import RecipeCommentUpdate
from mealie_mcp.client_factory import build_client
from mealie_mcp.tools._common import expect_dict, expect_list, require_non_empty, require_per_page


def create_comment(client: AuthenticatedClient, recipe_id: str, text: str) -> dict[str, Any]:
    """Create a comment on a recipe. Returns the new comment payload."""
    require_non_empty("recipe_id", recipe_id)
    require_non_empty("text", text)

    response = create_one_api_comments_post.sync_detailed(
        client=client, body=RecipeCommentCreate(recipe_id=recipe_id, text=text)
    )
    return expect_dict("create_comment", response, HTTPStatus.CREATED)


def get_comment(client: AuthenticatedClient, comment_id: str) -> dict[str, Any]:
    """Fetch a comment by id. Returns the comment payload."""
    require_non_empty("comment_id", comment_id)

    response = get_one_api_comments_item_id_get.sync_detailed(comment_id, client=client)
    return expect_dict("get_comment", response)


def list_comments(client: AuthenticatedClient, page: int = 1, per_page: int = 50) -> dict[str, Any]:
    """List all comments across recipes, paginated. Returns the page payload."""
    require_per_page(per_page)
    response = get_all_api_comments_get.sync_detailed(client=client, page=page, per_page=per_page)
    return expect_dict("list_comments", response)


def list_recipe_comments(client: AuthenticatedClient, slug: str) -> list[Any]:
    """List the comments attached to a recipe. Returns a list of comment payloads."""
    require_non_empty("slug", slug)

    response = get_recipe_comments_api_recipes_slug_comments_get.sync_detailed(slug, client=client)
    return expect_list("list_recipe_comments", response)


def update_comment(client: AuthenticatedClient, comment_id: str, text: str) -> dict[str, Any]:
    """Update the text of a comment. Returns the updated comment payload."""
    require_non_empty("comment_id", comment_id)
    require_non_empty("text", text)

    response = update_one_api_comments_item_id_put.sync_detailed(
        comment_id,
        client=client,
        body=RecipeCommentUpdate(id=comment_id, text=text),
    )
    return expect_dict("update_comment", response)


def delete_comment(client: AuthenticatedClient, comment_id: str) -> dict[str, Any]:
    """Delete a comment by id. Returns Mealie's success response payload."""
    require_non_empty("comment_id", comment_id)

    response = delete_one_api_comments_item_id_delete.sync_detailed(comment_id, client=client)
    return expect_dict("delete_comment", response)


def register(mcp: FastMCP) -> None:
    """Register the recipe comment tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_create_comment")
    def _create_comment(recipe_id: str, text: str) -> dict[str, Any]:
        """Create a comment on a Mealie recipe.

        Args:
            recipe_id: UUID of the recipe to comment on.
            text: Comment body. Required, must be non-empty.

        Returns:
            The newly created comment payload as a JSON-compatible dict.
        """
        return create_comment(build_client(), recipe_id=recipe_id, text=text)

    @mcp.tool(name="mealie_get_comment")
    def _get_comment(comment_id: str) -> dict[str, Any]:
        """Fetch a single comment from Mealie by id.

        Args:
            comment_id: UUID of the comment.

        Returns:
            The comment payload as a JSON-compatible dict.
        """
        return get_comment(build_client(), comment_id=comment_id)

    @mcp.tool(name="mealie_list_comments")
    def _list_comments(page: int = 1, per_page: int = 50) -> dict[str, Any]:
        """List all comments across all recipes, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50. Capped at 100.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_comments(build_client(), page=page, per_page=per_page)

    @mcp.tool(name="mealie_list_recipe_comments")
    def _list_recipe_comments(slug: str) -> list[Any]:
        """List the comments attached to a single recipe.

        Args:
            slug: Recipe slug.

        Returns:
            A list of comment payloads for the recipe.
        """
        return list_recipe_comments(build_client(), slug=slug)

    @mcp.tool(name="mealie_update_comment")
    def _update_comment(comment_id: str, text: str) -> dict[str, Any]:
        """Update the text of an existing comment.

        Args:
            comment_id: UUID of the comment to update.
            text: New comment body. Required, must be non-empty.

        Returns:
            The updated comment payload as a JSON-compatible dict.
        """
        return update_comment(build_client(), comment_id=comment_id, text=text)

    @mcp.tool(name="mealie_delete_comment")
    def _delete_comment(comment_id: str) -> dict[str, Any]:
        """Delete a comment from Mealie by id.

        Args:
            comment_id: UUID of the comment to delete.

        Returns:
            Mealie's success response payload as a JSON-compatible dict.
        """
        return delete_comment(build_client(), comment_id=comment_id)
