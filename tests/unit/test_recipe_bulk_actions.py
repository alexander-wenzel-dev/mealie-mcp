"""Input-validation tests for the recipe bulk-action tools.

The Mealie HTTP contract is exercised by
`tests/live/test_recipe_bulk_actions.py`; shared helper behaviour lives in
`tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_bulk_actions


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestTagRecipes:
    def test_rejects_empty_recipes(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipes must contain at least one slug"):
            recipe_bulk_actions.tag_recipes(client, recipes=[], tags=[{"name": "n"}])

    def test_rejects_blank_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe slug must be a non-empty string"):
            recipe_bulk_actions.tag_recipes(client, recipes=["  "], tags=[{"name": "n"}])

    def test_rejects_empty_tags(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="tags must contain at least one tag object"):
            recipe_bulk_actions.tag_recipes(client, recipes=["a"], tags=[])

    def test_rejects_malformed_tag(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="tag_recipes tags invalid"):
            recipe_bulk_actions.tag_recipes(client, recipes=["a"], tags=[{"name": "n"}])


class TestCategorizeRecipes:
    def test_rejects_empty_recipes(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipes must contain at least one slug"):
            recipe_bulk_actions.categorize_recipes(client, recipes=[], categories=[{"name": "n"}])

    def test_rejects_blank_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe slug must be a non-empty string"):
            recipe_bulk_actions.categorize_recipes(
                client, recipes=["  "], categories=[{"name": "n"}]
            )

    def test_rejects_empty_categories(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="categories must contain at least one category object"):
            recipe_bulk_actions.categorize_recipes(client, recipes=["a"], categories=[])

    def test_rejects_malformed_category(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="categorize_recipes categories invalid"):
            recipe_bulk_actions.categorize_recipes(
                client, recipes=["a"], categories=[{"name": "n"}]
            )


class TestApplyRecipeSettings:
    def test_rejects_empty_recipes(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipes must contain at least one slug"):
            recipe_bulk_actions.apply_recipe_settings(
                client,
                recipes=[],
                public=True,
                show_nutrition=False,
                show_assets=False,
                landscape_view=False,
                disable_comments=True,
            )

    def test_rejects_blank_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe slug must be a non-empty string"):
            recipe_bulk_actions.apply_recipe_settings(
                client,
                recipes=["  "],
                public=True,
                show_nutrition=False,
                show_assets=False,
                landscape_view=False,
                disable_comments=True,
            )


class TestDeleteRecipes:
    def test_rejects_empty_recipes(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipes must contain at least one slug"):
            recipe_bulk_actions.delete_recipes(client, recipes=[])

    def test_rejects_blank_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe slug must be a non-empty string"):
            recipe_bulk_actions.delete_recipes(client, recipes=["ok", ""])
