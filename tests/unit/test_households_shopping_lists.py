"""Input-validation tests for the household shopping list tools.

The Mealie HTTP contract is exercised by
`tests/live/test_households_shopping_lists.py`; shared helper behaviour lives in
`tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_shopping_lists


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListShoppingLists:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be <= 100 \(got 101\)"):
            households_shopping_lists.list_shopping_lists(client, per_page=101)


class TestCreateShoppingList:
    def test_rejects_blank_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            households_shopping_lists.create_shopping_list(client, name="   ")


class TestGetShoppingList:
    def test_rejects_blank_list_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="list_id must be a non-empty string"):
            households_shopping_lists.get_shopping_list(client, list_id="")


class TestUpdateShoppingList:
    def test_rejects_blank_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            households_shopping_lists.update_shopping_list(client, list_id="abc", name="")


class TestDeleteShoppingList:
    def test_rejects_blank_list_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="list_id must be a non-empty string"):
            households_shopping_lists.delete_shopping_list(client, list_id="   ")


class TestAddRecipeToShoppingList:
    def test_rejects_blank_list_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="list_id must be a non-empty string"):
            households_shopping_lists.add_recipe_to_shopping_list(
                client, list_id="", recipe_id="r1"
            )

    def test_rejects_blank_recipe_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a non-empty string"):
            households_shopping_lists.add_recipe_to_shopping_list(
                client, list_id="abc", recipe_id="   "
            )


class TestAddRecipesToShoppingList:
    def test_rejects_blank_list_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="list_id must be a non-empty string"):
            households_shopping_lists.add_recipes_to_shopping_list(
                client, list_id="", recipes=[{"recipe_id": "r1"}]
            )

    def test_rejects_empty_recipes(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipes must be a non-empty list"):
            households_shopping_lists.add_recipes_to_shopping_list(
                client, list_id="abc", recipes=[]
            )

    def test_rejects_entry_without_recipe_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="each recipe must include a recipe_id string"):
            households_shopping_lists.add_recipes_to_shopping_list(
                client, list_id="abc", recipes=[{"scale": 2.0}]
            )

    def test_rejects_blank_recipe_id_in_entry(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a non-empty string"):
            households_shopping_lists.add_recipes_to_shopping_list(
                client, list_id="abc", recipes=[{"recipe_id": "  "}]
            )

    def test_rejects_non_object_entry(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="each recipe must be an object with a recipe_id"):
            households_shopping_lists.add_recipes_to_shopping_list(
                client, list_id="abc", recipes=[42]
            )

    def test_rejects_non_numeric_scale(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="each recipe's scale must be a number"):
            households_shopping_lists.add_recipes_to_shopping_list(
                client, list_id="abc", recipes=[{"recipe_id": "r1", "scale": "two"}]
            )


class TestRemoveRecipeFromShoppingList:
    def test_rejects_blank_list_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="list_id must be a non-empty string"):
            households_shopping_lists.remove_recipe_from_shopping_list(
                client, list_id="   ", recipe_id="r1"
            )

    def test_rejects_blank_recipe_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a non-empty string"):
            households_shopping_lists.remove_recipe_from_shopping_list(
                client, list_id="abc", recipe_id=""
            )
