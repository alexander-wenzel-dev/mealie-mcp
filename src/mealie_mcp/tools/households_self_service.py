"""Household self-service tools.

Mirrors `mealie_mcp.client.api.households_self_service`. Exposes the current
household's record of a recipe, which carries the household's last-made
timestamp.
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from mealie_mcp.client.api.households_self_service import (
    get_household_recipe_api_households_self_recipes_recipe_slug_get,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import expect_dict, require_non_empty


def get_household_recipe(client: AuthenticatedClient, slug_or_id: str) -> dict[str, Any]:
    """Fetch the current household's record of a recipe. Returns the summary."""
    require_non_empty("slug_or_id", slug_or_id)

    response = get_household_recipe_api_households_self_recipes_recipe_slug_get.sync_detailed(
        slug_or_id, client=client
    )
    return expect_dict("get_household_recipe", response)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the household self-service tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_get_household_recipe")
    def _get_household_recipe(slug_or_id: str) -> dict[str, Any]:
        """Read when the current household last made a recipe.

        Mealie stores the last-made timestamp per household, so the recipe
        payload does not carry it. Set it with ``mealie_update_last_made``.

        Args:
            slug_or_id: Recipe slug or UUID.

        Returns:
            ``{"recipeId": <uuid>, "lastMade": <ISO 8601 datetime in UTC>}``.
            ``lastMade`` is null when the household never made the recipe.
        """
        return get_household_recipe(get_client(), slug_or_id=slug_or_id)
