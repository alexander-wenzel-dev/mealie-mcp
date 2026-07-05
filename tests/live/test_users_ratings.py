"""Live test for the user rating and favorite lifecycle.

Stages a sentinel recipe, sets a rating, toggles a favorite, and asserts each
change appears in the acting user's ratings and favorites listings. Cleanup
deletes the recipe even when the body fails, which also clears its rating.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_crud, users_ratings


@pytest.fixture
def created_recipe(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a recipe to rate and favorite, then tear it down."""
    created = recipe_crud.create_recipe(mealie_client, name=sentinel_name)
    slug = created["slug"]
    try:
        recipe = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        yield {"slug": slug, "id": recipe["id"]}
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_rating_and_favorite_lifecycle(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    slug = created_recipe["slug"]
    recipe_id = created_recipe["id"]

    rating_ack = users_ratings.set_recipe_rating(mealie_client, slug=slug, rating=4.5)
    assert rating_ack == {"slug": slug, "rating": 4.5}

    ratings = users_ratings.list_ratings(mealie_client)
    rated = next((r for r in ratings if r["recipeId"] == recipe_id), None)
    assert rated is not None, f"rating for {slug} not found in user ratings"
    assert rated["rating"] == 4.5

    add_ack = users_ratings.add_favorite(mealie_client, slug=slug)
    assert add_ack == {"slug": slug, "is_favorite": True}

    favorites = users_ratings.list_favorites(mealie_client)
    favorited = next((r for r in favorites if r["recipeId"] == recipe_id), None)
    assert favorited is not None, f"favorite for {slug} not found in user favorites"
    assert favorited["isFavorite"] is True

    # Setting a rating must not clear an existing favorite: set_recipe_rating
    # omits the unexposed is_favorite field, which would clobber it under
    # replace semantics.
    users_ratings.set_recipe_rating(mealie_client, slug=slug, rating=2.0)
    favorites_after_rating = users_ratings.list_favorites(mealie_client)
    still_favorited = next((r for r in favorites_after_rating if r["recipeId"] == recipe_id), None)
    assert still_favorited is not None, f"favorite for {slug} cleared by set_recipe_rating"
    assert still_favorited["isFavorite"] is True

    remove_ack = users_ratings.remove_favorite(mealie_client, slug=slug)
    assert remove_ack == {"id": slug, "deleted": True}

    after_removal = users_ratings.list_favorites(mealie_client)
    assert all(r["recipeId"] != recipe_id for r in after_removal)


@pytest.mark.live
def test_set_recipe_rating_round_trips_through_wrapper(
    created_recipe: dict[str, str],
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    slug = created_recipe["slug"]
    ack = call_tool("mealie_set_recipe_rating", {"slug": slug, "rating": 4.5})
    # The wrapper serializes the synthesized ack; the recipe fixture clears the rating on teardown.
    assert ack == {"slug": slug, "rating": 4.5}
