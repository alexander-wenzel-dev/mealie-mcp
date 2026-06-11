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
        with pytest.raises(ToolError, match=r"per_page must be <= 100 \(got 101\)"):
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


class TestUpdateUnit:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_units.update_unit(client, item_id="", name="new")

    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipes_units.update_unit(client, item_id="abc", name="")


class TestDeleteUnit:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            recipes_units.delete_unit(client, item_id="")
