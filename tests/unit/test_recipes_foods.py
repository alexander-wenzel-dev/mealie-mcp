"""Input-validation tests for the food tools.

The Mealie HTTP contract is exercised by `tests/live/test_recipes_foods.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipes_foods


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListFoods:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be <= 100 \(got 101\)"):
            recipes_foods.list_foods(client, per_page=101)


class TestGetFood:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_foods.get_food(client, item_id="")


class TestCreateFood:
    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_foods.create_food(client, name="")

    def test_rejects_whitespace_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_foods.create_food(client, name="   ")


class TestUpdateFood:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_foods.update_food(client, item_id="", name="new")

    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_foods.update_food(client, item_id="abc", name="")


class TestDeleteFood:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_foods.delete_food(client, item_id="")
