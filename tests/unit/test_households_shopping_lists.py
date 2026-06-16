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
