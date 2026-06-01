"""Input-validation tests for the recipe CRUD tools.

The Mealie HTTP contract is exercised by `tests/live/test_recipe_crud.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_crud


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestCreateRecipe:
    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipe_crud.create_recipe(client, name="")

    def test_rejects_whitespace_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipe_crud.create_recipe(client, name="   ")


class TestGetRecipe:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug_or_id must be a non-empty string"):
            recipe_crud.get_recipe(client, slug_or_id="")


class TestDeleteRecipe:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug_or_id must be a non-empty string"):
            recipe_crud.delete_recipe(client, slug_or_id="")


class TestDuplicateRecipe:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug_or_id must be a non-empty string"):
            recipe_crud.duplicate_recipe(client, slug_or_id="")


class TestUpdateLastMade:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug_or_id must be a non-empty string"):
            recipe_crud.update_last_made(client, slug_or_id="", timestamp="2026-06-01T00:00:00")

    def test_rejects_empty_timestamp(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="timestamp must be a non-empty string"):
            recipe_crud.update_last_made(client, slug_or_id="abc", timestamp="")

    def test_rejects_non_iso_timestamp(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="timestamp must be an ISO 8601 datetime"):
            recipe_crud.update_last_made(client, slug_or_id="abc", timestamp="yesterday")


class TestParseRecipeUrl:
    def test_rejects_empty_url(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="url must be a non-empty string"):
            recipe_crud.parse_recipe_url(client, url="")


class TestCreateRecipeFromHtmlOrJson:
    def test_rejects_empty_data(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="data must be a non-empty string"):
            recipe_crud.create_recipe_from_html_or_json(client, data="")
