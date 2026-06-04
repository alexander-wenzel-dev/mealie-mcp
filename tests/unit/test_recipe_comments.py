"""Input-validation tests for the recipe comment tools.

The Mealie HTTP contract is exercised by `tests/live/test_recipe_comments.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_comments


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestCreateComment:
    def test_rejects_empty_recipe_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a non-empty string"):
            recipe_comments.create_comment(client, recipe_id="", text="hi")

    def test_rejects_empty_text(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="text must be a non-empty string"):
            recipe_comments.create_comment(client, recipe_id="abc", text="   ")


class TestGetComment:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="comment_id must be a non-empty string"):
            recipe_comments.get_comment(client, comment_id="")


class TestListComments:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be <= 100 \(got 101\)"):
            recipe_comments.list_comments(client, per_page=101)


class TestListRecipeComments:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug must be a non-empty string"):
            recipe_comments.list_recipe_comments(client, slug="")


class TestUpdateComment:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="comment_id must be a non-empty string"):
            recipe_comments.update_comment(client, comment_id="", text="hi")

    def test_rejects_empty_text(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="text must be a non-empty string"):
            recipe_comments.update_comment(client, comment_id="abc", text="")


class TestDeleteComment:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="comment_id must be a non-empty string"):
            recipe_comments.delete_comment(client, comment_id="")
