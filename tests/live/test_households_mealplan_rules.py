"""Live tests for the household meal plan rule lifecycle.

Stages a sentinel rule and exercises the create, get, list, update, and delete
tools. The lifecycle test proves the create status and response shape, that
``day``, ``entry_type``, and ``query_filter_string`` round-trip, and that a
one-field update preserves the other two through fetch-then-merge, so a
regression that PUT-replaced with a sparse body would fail the test. A rule has
no user-facing display name, so the sentinel name is stored in the filter DSL
and rules are matched by their returned id. Cleanup runs even when the body
fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_mealplan_rules


@pytest.mark.live
def test_mealplan_rule_lifecycle(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    query_filter_string = f'tags.name CONTAINS ALL ["{sentinel_name}"]'
    rule_id: str | None = None
    try:
        created = households_mealplan_rules.create_mealplan_rule(
            mealie_client,
            day="monday",
            entry_type="dinner",
            query_filter_string=query_filter_string,
        )
        rule_id = created["id"]
        # The create response is a 201 body shaped as a rule.
        assert created["day"] == "monday"
        assert created["entryType"] == "dinner"
        assert created["queryFilterString"] == query_filter_string

        fetched = households_mealplan_rules.get_mealplan_rule(mealie_client, item_id=rule_id)
        assert fetched["day"] == "monday"
        assert fetched["entryType"] == "dinner"
        assert fetched["queryFilterString"] == query_filter_string

        listing = households_mealplan_rules.list_mealplan_rules(mealie_client, per_page=100)
        assert any(item["id"] == rule_id for item in listing["items"])

        # Update only the day. The entry type and filter are not supplied, so
        # fetch-then-merge must preserve them rather than reset them to defaults.
        updated = households_mealplan_rules.update_mealplan_rule(
            mealie_client, item_id=rule_id, day="friday"
        )
        assert updated["day"] == "friday"
        assert updated["entryType"] == "dinner"
        assert updated["queryFilterString"] == query_filter_string

        refetched = households_mealplan_rules.get_mealplan_rule(mealie_client, item_id=rule_id)
        assert refetched["day"] == "friday"
        assert refetched["entryType"] == "dinner"
        assert refetched["queryFilterString"] == query_filter_string

        ack = households_mealplan_rules.delete_mealplan_rule(mealie_client, item_id=rule_id)
        assert ack == {"id": rule_id, "deleted": True}
        deleted_id, rule_id = rule_id, None

        with pytest.raises(ToolError, match=r"Mealie get_mealplan_rule failed \(404"):
            households_mealplan_rules.get_mealplan_rule(mealie_client, item_id=deleted_id)
    finally:
        if rule_id is not None:
            with contextlib.suppress(ToolError):
                households_mealplan_rules.delete_mealplan_rule(mealie_client, item_id=rule_id)


@pytest.mark.live
def test_create_mealplan_rule_defaults_to_any_day_and_type(
    mealie_client: AuthenticatedClient,
) -> None:
    created = households_mealplan_rules.create_mealplan_rule(mealie_client)
    rule_id = created["id"]
    try:
        # Omitting day and entry_type stores Mealie's "unset" sentinel, meaning
        # the rule applies to any day and any meal type.
        assert created["day"] == "unset"
        assert created["entryType"] == "unset"
        fetched = households_mealplan_rules.get_mealplan_rule(mealie_client, item_id=rule_id)
        assert fetched["day"] == "unset"
        assert fetched["entryType"] == "unset"
    finally:
        with contextlib.suppress(ToolError):
            households_mealplan_rules.delete_mealplan_rule(mealie_client, item_id=rule_id)


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_create_mealplan_rule_round_trips_through_wrapper(
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    query_filter_string = f'tags.name CONTAINS ALL ["{sentinel_name}"]'
    created = call_tool(
        "mealie_create_mealplan_rule",
        {
            "day": "tuesday",
            "entry_type": "lunch",
            "query_filter_string": query_filter_string,
        },
    )
    assert isinstance(created, dict)
    item_id = created["id"]
    try:
        # Fetching all three back catches a wrapper that forwards an argument to
        # the wrong parameter.
        assert created["day"] == "tuesday"
        assert created["entryType"] == "lunch"
        assert created["queryFilterString"] == query_filter_string
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_mealplan_rule", {"item_id": item_id})
