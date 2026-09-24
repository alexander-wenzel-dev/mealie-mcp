"""Input-validation tests for the category tools.

The Mealie HTTP contract is exercised by `tests/live/test_organizer_categories.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import organizer_categories

ITEM_ID = "0b6c9a53-1f0e-4f7a-9d6e-3c2b8a7e5d41"


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListCategories:
    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be between 1 and 100 \(got 101\)"):
            organizer_categories.list_categories(client, per_page=101)


class TestGetCategory:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_categories.get_category(client, item_id="")


class TestGetCategoryBySlug:
    def test_rejects_empty_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="slug must be a non-empty string"):
            organizer_categories.get_category_by_slug(client, slug="")


class TestCreateCategory:
    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_categories.create_category(client, name="")

    def test_rejects_whitespace_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_categories.create_category(client, name="   ")


class TestUpdateCategory:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_categories.update_category(client, item_id="", name="new")

    def test_rejects_empty_name(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            organizer_categories.update_category(client, item_id="abc", name="")


class TestDeleteCategory:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="item_id must be a non-empty string"):
            organizer_categories.delete_category(client, item_id="")


class TestMergeCategory:
    def test_rejects_empty_source_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="from_category_id must be a non-empty string"):
            organizer_categories.merge_category(client, from_category_id="", to_category_id=ITEM_ID)

    def test_rejects_empty_target_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_category_id must be a non-empty string"):
            organizer_categories.merge_category(client, from_category_id=ITEM_ID, to_category_id="")

    def test_rejects_a_slug(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="to_category_id must be a UUID"):
            organizer_categories.merge_category(
                client, from_category_id=ITEM_ID, to_category_id="dinner"
            )

    @pytest.mark.parametrize(
        "to_category_id",
        [ITEM_ID, ITEM_ID.upper(), ITEM_ID.replace("-", ""), f"urn:uuid:{ITEM_ID}"],
    )
    def test_rejects_a_self_merge(self, client: AuthenticatedClient, to_category_id: str) -> None:
        with pytest.raises(ToolError, match="merge_category requires two different categories"):
            organizer_categories.merge_category(
                client, from_category_id=ITEM_ID, to_category_id=to_category_id
            )
