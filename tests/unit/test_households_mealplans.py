"""Input-validation tests for the household meal plan tools.

The Mealie HTTP contract is exercised by `tests/live/test_households_mealplans.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_mealplans


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListMealplans:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            households_mealplans.list_mealplans(client, per_page=101)

    def test_rejects_malformed_start_date(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="start_date must be an ISO 8601 date"):
            households_mealplans.list_mealplans(client, start_date="06-15-2026")

    def test_rejects_malformed_end_date(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="end_date must be an ISO 8601 date"):
            households_mealplans.list_mealplans(client, end_date="not-a-date")


class TestCreateMealplan:
    def test_rejects_malformed_date(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="date must be an ISO 8601 date"):
            households_mealplans.create_mealplan(client, date="15/06/2026")

    def test_rejects_non_uuid_recipe_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a recipe UUID"):
            households_mealplans.create_mealplan(client, date="2026-06-15", recipe_id="my-slug")

    def test_rejects_unknown_entry_type(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="entry_type must be one of"):
            households_mealplans.create_mealplan(client, date="2026-06-15", entry_type="brunch")


class TestCreateRandomMealplan:
    def test_rejects_malformed_date(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="date must be an ISO 8601 date"):
            households_mealplans.create_random_mealplan(client, date="15/06/2026")

    def test_rejects_empty_date(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="date must be an ISO 8601 date"):
            households_mealplans.create_random_mealplan(client, date="")

    def test_rejects_unknown_entry_type(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="entry_type must be one of"):
            households_mealplans.create_random_mealplan(
                client, date="2026-06-15", entry_type="brunch"
            )


class TestUpdateMealplan:
    def test_rejects_no_fields(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="requires at least one field to update"):
            households_mealplans.update_mealplan(client, item_id=1)

    def test_rejects_malformed_date(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="date must be an ISO 8601 date"):
            households_mealplans.update_mealplan(client, item_id=1, date="June 15")

    def test_rejects_unknown_entry_type(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="entry_type must be one of"):
            households_mealplans.update_mealplan(client, item_id=1, entry_type="brunch")
