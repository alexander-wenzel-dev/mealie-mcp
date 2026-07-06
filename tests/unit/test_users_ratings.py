"""Input-validation tests for the user rating and favorite tools.

The Mealie HTTP contract is exercised by `tests/live/test_users_ratings.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import users_ratings


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestSetRecipeRating:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug must be a non-empty string"):
            users_ratings.set_recipe_rating(client, slug="   ", rating=4.5)

    @pytest.mark.parametrize("rating", [6.0, -1.0])
    def test_rejects_out_of_range_rating(self, client: AuthenticatedClient, rating: float) -> None:
        with pytest.raises(ToolError, match=r"rating must be between 0 and 5 \(got"):
            users_ratings.set_recipe_rating(client, slug="valid-slug", rating=rating)


class TestCurrentUserId:
    def test_returns_cached_id_without_calling_the_client(
        self, client: AuthenticatedClient
    ) -> None:
        """A pre-seeded cache short-circuits the ``GET /api/users/self`` lookup.

        The client points at a host with no server, so a cache miss would raise
        on the HTTP call. Returning the seeded id proves the cache-hit path.
        """
        users_ratings._user_id_by_token[client.token] = "cached-user-id"
        try:
            assert users_ratings._current_user_id(client) == "cached-user-id"
        finally:
            users_ratings._user_id_by_token.pop(client.token, None)


class TestAddFavorite:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug must be a non-empty string"):
            users_ratings.add_favorite(client, slug="")


class TestRemoveFavorite:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug must be a non-empty string"):
            users_ratings.remove_favorite(client, slug="")
