"""Input-validation tests for the household cookbook tools.

The Mealie HTTP contract is exercised by
`tests/live/test_households_cookbooks.py`; shared helper behaviour lives in
`tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_cookbooks


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListCookbooks:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be <= 100 \(got 101\)"):
            households_cookbooks.list_cookbooks(client, per_page=101)


class TestCreateCookbook:
    def test_rejects_blank_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            households_cookbooks.create_cookbook(client, name="   ")


class TestGetCookbook:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_cookbooks.get_cookbook(client, item_id="")


class TestUpdateCookbook:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_cookbooks.update_cookbook(client, item_id="   ", name="x")

    def test_rejects_blank_name_when_provided(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            households_cookbooks.update_cookbook(client, item_id="abc", name="")

    def test_rejects_when_no_fields_supplied(self, client: AuthenticatedClient) -> None:
        with pytest.raises(
            ToolError, match="update_cookbook requires at least one field to update"
        ):
            households_cookbooks.update_cookbook(client, item_id="abc")


class TestDeleteCookbook:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            households_cookbooks.delete_cookbook(client, item_id="   ")
