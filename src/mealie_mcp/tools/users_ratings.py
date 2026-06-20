"""User rating and favorite tools.

Mirrors `mealie_mcp.client.api.users_ratings`. Exposes setting a recipe rating,
listing the acting user's ratings and favorites, and adding or removing a
favorite. The acting user is resolved from the authenticated token, so callers
reference recipes by slug and never supply a user id.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.users_crud import get_logged_in_user_api_users_self_get
from mealie_mcp.client.api.users_ratings import (
    add_favorite_api_users_id_favorites_slug_post,
    get_favorites_api_users_id_favorites_get,
    get_ratings_api_users_id_ratings_get,
    remove_favorite_api_users_id_favorites_slug_delete,
    set_rating_api_users_id_ratings_slug_post,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.user_rating_update import UserRatingUpdate
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    raise_api_error,
    require_non_empty,
)


def _current_user_id(client: AuthenticatedClient) -> str:
    """Resolve the acting user's id from the authenticated token."""
    response = get_logged_in_user_api_users_self_get.sync_detailed(client=client)
    user = expect_dict("resolve current user", response)
    user_id = user.get("id")
    if not isinstance(user_id, str) or not user_id:
        raise ToolError("Could not resolve the current user id from Mealie")
    return user_id


def _ratings_list(action: str, response: Any) -> list[Any]:
    """Pull the ``ratings`` array out of a user-rating collection envelope."""
    payload = expect_dict(action, response)
    ratings = payload.get("ratings")
    if not isinstance(ratings, list):
        raise ToolError(f"Unexpected {action} response: {payload!r}")
    return ratings


def set_recipe_rating(client: AuthenticatedClient, slug: str, rating: float) -> dict[str, Any]:
    """Set the acting user's rating for a recipe. Returns a confirmation."""
    require_non_empty("slug", slug)

    user_id = _current_user_id(client)
    response = set_rating_api_users_id_ratings_slug_post.sync_detailed(
        user_id, slug, client=client, body=UserRatingUpdate(rating=rating)
    )
    if response.status_code != HTTPStatus.OK:
        raise_api_error("set_recipe_rating", int(response.status_code), response.content)
    return {"slug": slug, "rating": rating}


def list_ratings(client: AuthenticatedClient) -> list[Any]:
    """List the acting user's recipe ratings. Returns a list of rating records."""
    user_id = _current_user_id(client)
    response = get_ratings_api_users_id_ratings_get.sync_detailed(user_id, client=client)
    return _ratings_list("list_ratings", response)


def list_favorites(client: AuthenticatedClient) -> list[Any]:
    """List the acting user's favorited recipes. Returns a list of favorited recipe records."""
    user_id = _current_user_id(client)
    response = get_favorites_api_users_id_favorites_get.sync_detailed(user_id, client=client)
    return _ratings_list("list_favorites", response)


def add_favorite(client: AuthenticatedClient, slug: str) -> dict[str, Any]:
    """Add a recipe to the acting user's favorites. Returns a confirmation."""
    require_non_empty("slug", slug)

    user_id = _current_user_id(client)
    response = add_favorite_api_users_id_favorites_slug_post.sync_detailed(
        user_id, slug, client=client
    )
    if response.status_code != HTTPStatus.OK:
        raise_api_error("add_favorite", int(response.status_code), response.content)
    return {"slug": slug, "is_favorite": True}


def remove_favorite(client: AuthenticatedClient, slug: str) -> dict[str, Any]:
    """Remove a recipe from the acting user's favorites. Returns an acknowledgement."""
    require_non_empty("slug", slug)

    user_id = _current_user_id(client)
    response = remove_favorite_api_users_id_favorites_slug_delete.sync_detailed(
        user_id, slug, client=client
    )
    return ack_delete("remove_favorite", response, slug)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the user rating and favorite tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_set_recipe_rating")
    def _set_recipe_rating(slug: str, rating: float) -> dict[str, Any]:
        """Set the current user's rating for a Mealie recipe.

        Args:
            slug: Recipe slug.
            rating: Numeric rating to store for the recipe.

        Returns:
            A confirmation ``{"slug": <slug>, "rating": <rating>}``.
        """
        return set_recipe_rating(get_client(), slug=slug, rating=rating)

    @mcp.tool(name="mealie_list_ratings")
    def _list_ratings() -> list[Any]:
        """List the current user's recipe ratings.

        Returns:
            A list of rating records, each with the recipe id, rating, and
            favorite flag.
        """
        return list_ratings(get_client())

    @mcp.tool(name="mealie_list_favorites")
    def _list_favorites() -> list[Any]:
        """List the current user's favorited recipes.

        Returns:
            A list of favorited recipe records for the recipes the user has
            favorited.
        """
        return list_favorites(get_client())

    @mcp.tool(name="mealie_add_favorite")
    def _add_favorite(slug: str) -> dict[str, Any]:
        """Add a Mealie recipe to the current user's favorites.

        Args:
            slug: Recipe slug to favorite.

        Returns:
            A confirmation ``{"slug": <slug>, "is_favorite": True}``.
        """
        return add_favorite(get_client(), slug=slug)

    @mcp.tool(name="mealie_remove_favorite")
    def _remove_favorite(slug: str) -> dict[str, Any]:
        """Remove a Mealie recipe from the current user's favorites.

        Args:
            slug: Recipe slug to unfavorite.

        Returns:
            A canonical acknowledgement ``{"id": <slug>, "deleted": True}``.
        """
        return remove_favorite(get_client(), slug=slug)
