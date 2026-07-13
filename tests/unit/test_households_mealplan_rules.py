"""Input-validation tests for the household meal plan rule tools.

The Mealie HTTP contract is exercised by
`tests/live/test_households_mealplan_rules.py`; shared helper behaviour lives in
`tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_mealplan_rules


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListMealplanRules:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            households_mealplan_rules.list_mealplan_rules(client, per_page=101)


class TestCreateMealplanRule:
    def test_rejects_invalid_day(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="day must be one of:"):
            households_mealplan_rules.create_mealplan_rule(client, day="funday")

    def test_rejects_invalid_entry_type(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="entry_type must be one of:"):
            households_mealplan_rules.create_mealplan_rule(client, entry_type="brunch")


class TestGetMealplanRule:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_mealplan_rules.get_mealplan_rule(client, item_id="")


class TestUpdateMealplanRule:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_mealplan_rules.update_mealplan_rule(client, item_id="   ", day="monday")

    def test_rejects_when_no_fields_supplied(self, client: AuthenticatedClient) -> None:
        with pytest.raises(
            ToolError, match="update_mealplan_rule requires at least one field to update"
        ):
            households_mealplan_rules.update_mealplan_rule(client, item_id="abc")

    def test_rejects_invalid_day(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="day must be one of:"):
            households_mealplan_rules.update_mealplan_rule(client, item_id="abc", day="funday")

    def test_rejects_invalid_entry_type(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="entry_type must be one of:"):
            households_mealplan_rules.update_mealplan_rule(
                client, item_id="abc", entry_type="brunch"
            )


class TestDeleteMealplanRule:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_mealplan_rules.delete_mealplan_rule(client, item_id="   ")
