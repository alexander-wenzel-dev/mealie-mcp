"""Input-validation tests for the household shopping list item tools.

The Mealie HTTP contract is exercised by
`tests/live/test_households_shopping_list_items.py`; shared helper behaviour
lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_shopping_list_items


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListShoppingListItems:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            households_shopping_list_items.list_shopping_list_items(client, per_page=101)

    def test_rejects_invalid_order_direction(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="order_direction must be 'asc' or 'desc'"):
            households_shopping_list_items.list_shopping_list_items(
                client, order_direction="sideways"
            )


class TestAddShoppingListItem:
    def test_rejects_blank_shopping_list_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="shopping_list_id must be a non-empty string"):
            households_shopping_list_items.add_shopping_list_item(
                client, shopping_list_id="", note="milk"
            )

    def test_rejects_blank_note(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="note must be a non-empty string"):
            households_shopping_list_items.add_shopping_list_item(
                client, shopping_list_id="abc", note="   "
            )


class TestUpdateShoppingListItem:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_shopping_list_items.update_shopping_list_item(client, item_id="", note="x")

    def test_rejects_no_fields(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="requires at least one field to update"):
            households_shopping_list_items.update_shopping_list_item(client, item_id="abc")


class TestDeleteShoppingListItem:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_shopping_list_items.delete_shopping_list_item(client, item_id="   ")


class TestDeleteShoppingListItemsBulk:
    def test_rejects_empty_list(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_ids must contain at least one id"):
            households_shopping_list_items.delete_shopping_list_items_bulk(client, item_ids=[])

    def test_rejects_blank_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_shopping_list_items.delete_shopping_list_items_bulk(
                client, item_ids=["abc", "   "]
            )
