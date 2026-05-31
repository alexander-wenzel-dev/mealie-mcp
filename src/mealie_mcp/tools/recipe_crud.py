"""Recipe CRUD tools.

Mirrors `mealie_mcp.client.api.recipe_crud`. Exposes the three operations that
form a recipe's lifecycle: create, read by slug or id, and delete.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipe_crud import (
    create_one_api_recipes_post,
    delete_one_api_recipes_slug_delete,
    get_one_api_recipes_slug_get,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_recipe import CreateRecipe
from mealie_mcp.client_factory import build_client
from mealie_mcp.tools._common import decode, raise_api_error, require_non_empty


def create_recipe(client: AuthenticatedClient, name: str) -> dict[str, str]:
    """Create a recipe with the given name. Returns ``{"slug": ...}``."""
    require_non_empty("name", name)

    response = create_one_api_recipes_post.sync_detailed(
        client=client, body=CreateRecipe(name=name)
    )
    if response.status_code != HTTPStatus.CREATED:
        raise_api_error("create_recipe", int(response.status_code), response.content)
    slug = decode(response.content)
    if not isinstance(slug, str):
        raise ToolError(f"Unexpected create_recipe response: {slug!r}")
    return {"slug": slug}


def get_recipe(client: AuthenticatedClient, slug_or_id: str) -> dict[str, Any]:
    """Fetch a recipe by slug or id. Returns the full recipe payload."""
    require_non_empty("slug_or_id", slug_or_id)

    response = get_one_api_recipes_slug_get.sync_detailed(slug_or_id, client=client)
    if response.status_code != HTTPStatus.OK:
        raise_api_error("get_recipe", int(response.status_code), response.content)
    payload = decode(response.content)
    if not isinstance(payload, dict):
        raise ToolError(f"Unexpected get_recipe response: {payload!r}")
    return payload


def delete_recipe(client: AuthenticatedClient, slug_or_id: str) -> dict[str, Any]:
    """Delete a recipe by slug or id. Returns the deleted recipe payload."""
    require_non_empty("slug_or_id", slug_or_id)

    response = delete_one_api_recipes_slug_delete.sync_detailed(slug_or_id, client=client)
    if response.status_code != HTTPStatus.OK:
        raise_api_error("delete_recipe", int(response.status_code), response.content)
    payload = decode(response.content)
    if not isinstance(payload, dict):
        return {"deleted": slug_or_id}
    return payload


def register(mcp: FastMCP) -> None:
    """Register the recipe CRUD tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_create_recipe")
    def _create_recipe(name: str) -> dict[str, str]:
        """Create a recipe in Mealie.

        Args:
            name: Human readable recipe name. Required, must be non-empty.

        Returns:
            ``{"slug": <slug>}`` where ``slug`` is the URL-safe identifier
            Mealie assigned to the new recipe.
        """
        return create_recipe(build_client(), name=name)

    @mcp.tool(name="mealie_get_recipe")
    def _get_recipe(slug_or_id: str) -> dict[str, Any]:
        """Fetch a single recipe from Mealie by slug or id.

        Args:
            slug_or_id: A recipe slug (e.g. ``"my-recipe"``) or UUID.

        Returns:
            The full Mealie recipe payload as a JSON-compatible dict.
        """
        return get_recipe(build_client(), slug_or_id=slug_or_id)

    @mcp.tool(name="mealie_delete_recipe")
    def _delete_recipe(slug_or_id: str) -> dict[str, Any]:
        """Delete a recipe from Mealie by slug or id.

        Args:
            slug_or_id: A recipe slug or UUID.

        Returns:
            The deleted recipe payload as a JSON-compatible dict.
        """
        return delete_recipe(build_client(), slug_or_id=slug_or_id)
