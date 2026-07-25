"""Live tests for the household meal plan rule lifecycle.

Stages a sentinel rule and exercises the create, get, list, update, and delete
tools. The lifecycle test proves the create status and response shape, that
``day``, ``entry_type``, and ``query_filter_string`` round-trip, and that a
one-field update preserves the other two through fetch-then-merge, so a
regression that PUT-replaced with a sparse body would fail the test. A rule has
no user-facing display name, so the sentinel name is stored in the filter DSL
and rules are matched by their returned id. A separate test stages two rules
that match the same slot and pins how Mealie combines them. Cleanup runs even
when the body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
import datetime as dt
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import (
    households_mealplan_rules,
    households_mealplans,
    organizer_tags,
    recipe_bulk_actions,
    recipe_crud,
)


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


@pytest.fixture
def tagged_recipes(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Stage two sentinel tags and three recipes: one per tag, one carrying both."""
    tags: list[dict[str, Any]] = []
    slugs: dict[str, str] = {}
    try:
        # Recording each tag as it is created means a failure on the second one
        # still tears down the first.
        for suffix in "ab":
            tags.append(organizer_tags.create_tag(mealie_client, name=f"{sentinel_name}-{suffix}"))
        for label, applied in (("a", tags[:1]), ("b", tags[1:]), ("both", tags)):
            slug = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-{label}")["slug"]
            slugs[label] = slug
            recipe_bulk_actions.tag_recipes(mealie_client, recipes=[slug], tags=applied)
        yield {
            "tag_a": tags[0]["name"],
            "tag_b": tags[1]["name"],
            **{f"slug_{label}": slug for label, slug in slugs.items()},
        }
    finally:
        for slug in slugs.values():
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
        for tag in tags:
            with contextlib.suppress(ToolError):
                organizer_tags.delete_tag(mealie_client, item_id=tag["id"])


@pytest.mark.live
def test_rules_matching_one_slot_intersect_rather_than_override(
    mealie_client: AuthenticatedClient,
    tagged_recipes: dict[str, str],
) -> None:
    monday = dt.date(2030, 1, 7)
    tuesday = monday + dt.timedelta(days=1)
    assert monday.strftime("%A") == "Monday"
    tag_a, tag_b = tagged_recipes["tag_a"], tagged_recipes["tag_b"]
    filter_a = f'tags.name CONTAINS ALL ["{tag_a}"]'
    entry_ids: list[int] = []
    rule_ids: list[str] = []

    def draw(date: dt.date) -> str:
        created = households_mealplans.create_random_mealplan(
            mealie_client, date=date.isoformat(), entry_type="dinner"
        )
        entry_ids.append(created["id"])
        return created["recipeId"]

    try:
        any_day = households_mealplan_rules.create_mealplan_rule(
            mealie_client, day="unset", entry_type="dinner", query_filter_string=filter_a
        )
        rule_ids.append(any_day["id"])
        monday_only = households_mealplan_rules.create_mealplan_rule(
            mealie_client,
            day="monday",
            entry_type="dinner",
            query_filter_string=f'tags.name CONTAINS ALL ["{tag_b}"]',
        )
        rule_ids.append(monday_only["id"])

        # Control: on Tuesday only the any-day rule matches, so its filter alone
        # decides and a tag-a recipe is reachable. Without this the Monday result
        # below could just mean the any-day rule never applied.
        tuesday_pick = recipe_crud.get_recipe(mealie_client, slug_or_id=draw(tuesday))
        assert {tag_a} <= {tag["name"] for tag in tuesday_pick["tags"]}

        # On Monday both rules match. Under override the Monday rule would pick a
        # tag-b recipe; under a union either tag would do. Mealie ANDs the two
        # filters instead, and two filters on the same relation match no recipe,
        # so the pick fails even though one staged recipe carries both tags.
        with pytest.raises(ToolError, match=r"Mealie create_random_mealplan failed \(404"):
            draw(monday)

        # The same requirement written as one filter is satisfiable, which is the
        # shape the tool docstring tells callers to use instead of stacking rules.
        households_mealplan_rules.delete_mealplan_rule(mealie_client, item_id=monday_only["id"])
        rule_ids.remove(monday_only["id"])
        households_mealplan_rules.update_mealplan_rule(
            mealie_client,
            item_id=any_day["id"],
            query_filter_string=f'tags.name CONTAINS ALL ["{tag_a}","{tag_b}"]',
        )
        combined_pick = draw(monday)
        assert (
            combined_pick
            == recipe_crud.get_recipe(mealie_client, slug_or_id=tagged_recipes["slug_both"])["id"]
        )
    finally:
        for entry_id in entry_ids:
            with contextlib.suppress(ToolError):
                households_mealplans.delete_mealplan(mealie_client, item_id=entry_id)
        for rule_id in rule_ids:
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
