"""Input-validation tests for the tool (equipment) tools.

The Mealie HTTP contract is exercised by `tests/live/test_organizer_tools.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import organizer_tools

ITEM_ID = "0b6c9a53-1f0e-4f7a-9d6e-3c2b8a7e5d41"


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListTools:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            organizer_tools.list_tools(client, per_page=101)


class TestGetTool:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_tools.get_tool(client, item_id="")


class TestGetToolBySlug:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug must be a non-empty string"):
            organizer_tools.get_tool_by_slug(client, slug="")


class TestCreateTool:
    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_tools.create_tool(client, name="")

    def test_rejects_whitespace_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_tools.create_tool(client, name="   ")


class TestUpdateTool:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_tools.update_tool(client, item_id="", name="new")

    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_tools.update_tool(client, item_id="abc", name="")


class TestDeleteTool:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_tools.delete_tool(client, item_id="")


class TestMergeTool:
    def test_rejects_empty_source_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="from_tool_id must be a non-empty string"):
            organizer_tools.merge_tool(client, from_tool_id="", to_tool_id=ITEM_ID)

    def test_rejects_empty_target_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_tool_id must be a non-empty string"):
            organizer_tools.merge_tool(client, from_tool_id=ITEM_ID, to_tool_id="")

    def test_rejects_a_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_tool_id must be a UUID"):
            organizer_tools.merge_tool(client, from_tool_id=ITEM_ID, to_tool_id="oven")

    @pytest.mark.parametrize(
        "to_tool_id",
        [ITEM_ID, ITEM_ID.upper(), ITEM_ID.replace("-", ""), f"urn:uuid:{ITEM_ID}"],
    )
    def test_rejects_a_self_merge(self, client: AuthenticatedClient, to_tool_id: str) -> None:
        with pytest.raises(ToolError, match="merge_tool requires two different tools"):
            organizer_tools.merge_tool(client, from_tool_id=ITEM_ID, to_tool_id=to_tool_id)
