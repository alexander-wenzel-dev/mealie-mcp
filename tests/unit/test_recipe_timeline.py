"""Input-validation tests for the recipe timeline tools.

The Mealie HTTP contract is exercised by `tests/live/test_recipe_timeline.py`;
shared helper behaviour lives in `tests/unit/test_common.py`.
"""

from __future__ import annotations

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_timeline


@pytest.fixture
def client() -> AuthenticatedClient:
    """Client whose HTTP path is never reached because validation raises first."""
    return AuthenticatedClient(base_url="https://mealie.example.com", token="t")


class TestListRecipeTimelineEvents:
    def test_rejects_empty_recipe_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a non-empty string"):
            recipe_timeline.list_recipe_timeline_events(client, recipe_id="")

    def test_rejects_per_page_above_max(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match=r"per_page must be <= 100 \(got 101\)"):
            recipe_timeline.list_recipe_timeline_events(client, recipe_id="abc", per_page=101)

    def test_rejects_bad_order_direction(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="order_direction must be 'asc' or 'desc'"):
            recipe_timeline.list_recipe_timeline_events(
                client,
                recipe_id="abc",
                order_direction="sideways",
            )


class TestCreateTimelineEvent:
    def test_rejects_empty_recipe_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a non-empty string"):
            recipe_timeline.create_timeline_event(client, recipe_id="", subject="made it")

    def test_rejects_empty_subject(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="subject must be a non-empty string"):
            recipe_timeline.create_timeline_event(client, recipe_id="abc", subject="  ")

    def test_rejects_system_event_type(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="event_type must be 'comment' or 'info'"):
            recipe_timeline.create_timeline_event(
                client, recipe_id="abc", subject="s", event_type="system"
            )

    def test_rejects_unknown_event_type(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="event_type must be 'comment' or 'info'"):
            recipe_timeline.create_timeline_event(
                client, recipe_id="abc", subject="s", event_type="banana"
            )

    def test_rejects_malformed_timestamp(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="timestamp must be an ISO 8601 datetime"):
            recipe_timeline.create_timeline_event(
                client, recipe_id="abc", subject="s", timestamp="not-a-date"
            )


class TestGetTimelineEvent:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="event_id must be a non-empty string"):
            recipe_timeline.get_timeline_event(client, event_id="")


class TestUpdateTimelineEvent:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="event_id must be a non-empty string"):
            recipe_timeline.update_timeline_event(client, event_id="", subject="s")

    def test_rejects_no_fields(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="requires subject or event_message"):
            recipe_timeline.update_timeline_event(client, event_id="abc")

    def test_rejects_empty_subject(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="subject must be a non-empty string"):
            recipe_timeline.update_timeline_event(client, event_id="abc", subject="   ")


class TestDeleteTimelineEvent:
    def test_rejects_empty_id(self, client: AuthenticatedClient) -> None:
        with pytest.raises(ToolError, match="event_id must be a non-empty string"):
            recipe_timeline.delete_timeline_event(client, event_id="")
