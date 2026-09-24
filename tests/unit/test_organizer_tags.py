"""Input-validation tests for the tag tools.

The Mealie HTTP contract is exercised by `tests/live/test_organizer_tags.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import organizer_tags

ITEM_ID = "0b6c9a53-1f0e-4f7a-9d6e-3c2b8a7e5d41"


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListTags:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            organizer_tags.list_tags(client, per_page=101)


class TestGetTag:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_tags.get_tag(client, item_id="")


class TestGetTagBySlug:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug must be a non-empty string"):
            organizer_tags.get_tag_by_slug(client, slug="")


class TestCreateTag:
    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_tags.create_tag(client, name="")

    def test_rejects_whitespace_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_tags.create_tag(client, name="   ")


class TestUpdateTag:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_tags.update_tag(client, item_id="", name="new")

    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_tags.update_tag(client, item_id="abc", name="")


class TestDeleteTag:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_tags.delete_tag(client, item_id="")


class TestMergeTag:
    def test_rejects_empty_source_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="from_tag_id must be a non-empty string"):
            organizer_tags.merge_tag(client, from_tag_id="", to_tag_id=ITEM_ID)

    def test_rejects_empty_target_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_tag_id must be a non-empty string"):
            organizer_tags.merge_tag(client, from_tag_id=ITEM_ID, to_tag_id="")

    def test_rejects_a_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_tag_id must be a UUID"):
            organizer_tags.merge_tag(client, from_tag_id=ITEM_ID, to_tag_id="dinner")

    @pytest.mark.parametrize(
        "to_tag_id",
        [ITEM_ID, ITEM_ID.upper(), ITEM_ID.replace("-", ""), f"urn:uuid:{ITEM_ID}"],
    )
    def test_rejects_a_self_merge(self, client: AuthenticatedClient, to_tag_id: str) -> None:
        with pytest.raises(ToolError, match="merge_tag requires two different tags"):
            organizer_tags.merge_tag(client, from_tag_id=ITEM_ID, to_tag_id=to_tag_id)
