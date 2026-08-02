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
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
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

    def test_rejects_blank_alias(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="aliases entry must be a non-empty string"):
            recipes_foods.create_food(client, name="butter", aliases=["ok", "   "])

    def test_rejects_empty_label_id(self, client: AuthenticatedClient) -> None:
        # An empty label_id means "detach" on update, but there is nothing to
        # detach on create, and Mealie answers the empty labelId with a 422.
        with pytest.raises(ToolError, match="label_id must be a non-empty string"):
            recipes_foods.create_food(client, name="butter", label_id="")


class TestUpdateFood:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_foods.update_food(client, item_id="", name="new")

    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_foods.update_food(client, item_id="abc", name="")

    def test_rejects_call_without_fields(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="update_food requires at least one field to update"):
            recipes_foods.update_food(client, item_id="abc")

    def test_rejects_blank_alias(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="aliases entry must be a non-empty string"):
            recipes_foods.update_food(client, item_id="abc", aliases=[""])


class TestDeleteFood:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_foods.delete_food(client, item_id="")


FOOD_ID = "8b6a6a1e-0d4e-4a2b-9a1f-2c3d4e5f6a7b"


class TestMergeFood:
    def test_rejects_empty_source_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="from_food_id must be a non-empty string"):
            recipes_foods.merge_food(client, from_food_id="", to_food_id=FOOD_ID)

    def test_rejects_empty_target_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_food_id must be a non-empty string"):
            recipes_foods.merge_food(client, from_food_id=FOOD_ID, to_food_id="")

    def test_rejects_a_malformed_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="from_food_id must be a UUID"):
            recipes_foods.merge_food(client, from_food_id="butter", to_food_id=FOOD_ID)

    @pytest.mark.parametrize(
        "to_food_id",
        [FOOD_ID, FOOD_ID.upper(), FOOD_ID.replace("-", ""), f"urn:uuid:{FOOD_ID}"],
    )
    def test_rejects_a_self_merge(self, client: AuthenticatedClient, to_food_id: str) -> None:
        # Mealie resolves each of these spellings to the same food, so a raw
        # string comparison would let the merge through and delete it.
        with pytest.raises(ToolError, match="merge_food requires two different foods"):
            recipes_foods.merge_food(client, from_food_id=FOOD_ID, to_food_id=to_food_id)
