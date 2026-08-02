"""Input-validation tests for the unit tools.

The Mealie HTTP contract is exercised by `tests/live/test_recipes_units.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipes_units


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListUnits:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            recipes_units.list_units(client, per_page=101)


class TestGetUnit:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_units.get_unit(client, item_id="")


class TestCreateUnit:
    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_units.create_unit(client, name="")

    def test_rejects_whitespace_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_units.create_unit(client, name="   ")

    def test_rejects_blank_alias(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="aliases entry must be a non-empty string"):
            recipes_units.create_unit(client, name="tablespoon", aliases=["ok", "   "])


class TestUpdateUnit:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_units.update_unit(client, item_id="", name="new")

    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_units.update_unit(client, item_id="abc", name="")

    def test_rejects_call_without_fields(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="update_unit requires at least one field to update"):
            recipes_units.update_unit(client, item_id="abc")

    def test_rejects_blank_alias(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="aliases entry must be a non-empty string"):
            recipes_units.update_unit(client, item_id="abc", aliases=[""])


class TestDeleteUnit:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_units.delete_unit(client, item_id="")


UNIT_ID = "3f2a1b0c-9d8e-4f6a-8b7c-1d2e3f4a5b6c"


class TestMergeUnit:
    def test_rejects_empty_source_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="from_unit_id must be a non-empty string"):
            recipes_units.merge_unit(client, from_unit_id="", to_unit_id=UNIT_ID)

    def test_rejects_empty_target_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_unit_id must be a non-empty string"):
            recipes_units.merge_unit(client, from_unit_id=UNIT_ID, to_unit_id="")

    def test_rejects_a_malformed_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="from_unit_id must be a UUID"):
            recipes_units.merge_unit(client, from_unit_id="gram", to_unit_id=UNIT_ID)

    @pytest.mark.parametrize(
        "to_unit_id",
        [UNIT_ID, UNIT_ID.upper(), UNIT_ID.replace("-", ""), f"urn:uuid:{UNIT_ID}"],
    )
    def test_rejects_a_self_merge(self, client: AuthenticatedClient, to_unit_id: str) -> None:
        # Mealie resolves each of these spellings to the same unit, so a raw
        # string comparison would let the merge through and delete it.
        with pytest.raises(ToolError, match="merge_unit requires two different units"):
            recipes_units.merge_unit(client, from_unit_id=UNIT_ID, to_unit_id=to_unit_id)
