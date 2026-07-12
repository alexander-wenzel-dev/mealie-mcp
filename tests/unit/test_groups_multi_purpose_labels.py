"""Input-validation tests for the multi purpose label tools.

The Mealie HTTP contract is exercised by
`tests/live/test_groups_multi_purpose_labels.py`; shared helper behaviour lives
in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import groups_multi_purpose_labels


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListLabels:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            groups_multi_purpose_labels.list_labels(client, per_page=101)


class TestCreateLabel:
    def test_rejects_blank_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            groups_multi_purpose_labels.create_label(client, name="   ")


class TestGetLabel:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            groups_multi_purpose_labels.get_label(client, item_id="")


class TestUpdateLabel:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            groups_multi_purpose_labels.update_label(client, item_id="   ", name="x")

    def test_rejects_blank_name_when_provided(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            groups_multi_purpose_labels.update_label(client, item_id="abc", name="")

    def test_rejects_when_no_fields_supplied(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="update_label requires at least one field to update"):
            groups_multi_purpose_labels.update_label(client, item_id="abc")


class TestDeleteLabel:
    def test_rejects_blank_item_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            groups_multi_purpose_labels.delete_label(client, item_id="   ")
