"""Live test for the household meal plan entry lifecycle.

Stages a sentinel recipe, schedules a sentinel meal plan entry that references
it, exercises the get, list, update, and delete tools, then tears both
sentinels down. The update step changes only ``text`` and asserts that the
unsupplied ``recipe_id`` link and ``entry_type`` survive the PUT-replace, so a
regression in fetch-then-merge would fail the test. Separate tests omit
``entry_type`` on each create tool and pin the differing slots Mealie seeds, and
one stages a rule whose filter matches nothing to pin what an unmatched rule
does. Others create week entries, pin the 422s for an off-span end date and a
non-positive scale, and change and remove the recipe, scale and week through
the update tool. Cleanup runs even when the test body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
import datetime as dt
from collections.abc import Callable, Iterator
from http import HTTPStatus
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_meal_plans import create_one_api_households_mealplans_post
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.plan_entry_create import PlanEntryCreate
from mealie_mcp.tools import households_meal_plan_rules, households_meal_plans, recipe_crud
from mealie_mcp.tools._common import expect_dict


@pytest.fixture
def created_recipe(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a recipe so a meal plan entry has something to reference."""
    created = recipe_crud.create_recipe(mealie_client, name=sentinel_name)
    slug = created["slug"]
    try:
        recipe = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        yield {"slug": slug, "id": recipe["id"]}
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.fixture
def created_mealplan(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
) -> Iterator[dict[str, object]]:
    """Schedule a sentinel meal plan entry referencing the recipe and tear it down."""
    plan_date = dt.date(2030, 1, 1)
    title = sentinel_name
    created = households_meal_plans.create_mealplan(
        mealie_client,
        date=plan_date.isoformat(),
        recipe_id=created_recipe["id"],
        title=title,
        entry_type="dinner",
    )
    item_id = created["id"]
    try:
        yield {
            "id": item_id,
            "date": plan_date,
            "recipe_id": created_recipe["id"],
            "title": title,
        }
    finally:
        with contextlib.suppress(ToolError):
            households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)


@pytest.mark.live
def test_mealplan_lifecycle(
    mealie_client: AuthenticatedClient,
    created_mealplan: dict[str, object],
    sentinel_name: str,
) -> None:
    item_id = created_mealplan["id"]
    plan_date: dt.date = created_mealplan["date"]
    recipe_id = created_mealplan["recipe_id"]
    title = created_mealplan["title"]
    note = f"{sentinel_name}-note"

    fetched = households_meal_plans.get_mealplan(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["recipeId"] == recipe_id
    assert fetched["title"] == title
    assert fetched["entryType"] == "dinner"

    listing = households_meal_plans.list_mealplans(
        mealie_client,
        start_date=plan_date.isoformat(),
        end_date=plan_date.isoformat(),
        per_page=100,
    )
    assert any(entry["id"] == item_id for entry in listing["items"])

    # An entry outside the requested range must not appear.
    other_day = households_meal_plans.list_mealplans(
        mealie_client,
        start_date=(plan_date + dt.timedelta(days=1)).isoformat(),
        end_date=(plan_date + dt.timedelta(days=1)).isoformat(),
        per_page=100,
    )
    assert all(entry["id"] != item_id for entry in other_day["items"])

    # Update only the note. The recipe link, title, and entry_type are not
    # supplied, so they must be preserved by fetch-then-merge rather than reset.
    updated = households_meal_plans.update_mealplan(mealie_client, item_id=item_id, text=note)
    assert updated["text"] == note
    assert updated["recipeId"] == recipe_id
    assert updated["title"] == title
    assert updated["entryType"] == "dinner"

    # A supplied field changes; the date moves and the recipe link still holds.
    new_date = plan_date + dt.timedelta(days=2)
    moved = households_meal_plans.update_mealplan(
        mealie_client, item_id=item_id, date=new_date.isoformat(), entry_type="lunch"
    )
    assert moved["date"] == new_date.isoformat()
    assert moved["entryType"] == "lunch"
    assert moved["text"] == note
    assert moved["recipeId"] == recipe_id

    ack = households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)
    assert ack == {"id": str(item_id), "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_mealplan failed \(404"):
        households_meal_plans.get_mealplan(mealie_client, item_id=item_id)


@pytest.mark.live
def test_week_entry_is_listed_on_request_and_keeps_its_span_on_update(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """A week entry keeps its span and scale through an update, and a moved date moves the span."""
    plan_date = dt.date(2030, 1, 7)
    span = dt.timedelta(days=6)
    item_id: int | None = None
    try:
        created = call_tool(
            "mealie_create_mealplan",
            {
                "date": plan_date.isoformat(),
                "end_date": (plan_date + span).isoformat(),
                "recipe_id": created_recipe["id"],
                "recipe_scale": 2.5,
                "title": sentinel_name,
            },
        )
        assert isinstance(created, dict)
        item_id = created["id"]
        assert created["endDate"] == (plan_date + span).isoformat()
        assert created["recipeScale"] == 2.5

        mid_week = (plan_date + dt.timedelta(days=3)).isoformat()
        listed: dict[bool, set[int]] = {}
        for include in (False, True):
            page = call_tool(
                "mealie_list_mealplans",
                {"start_date": mid_week, "end_date": mid_week, "include_week_entries": include},
            )
            assert isinstance(page, dict)
            listed[include] = {entry["id"] for entry in page["items"]}
        assert item_id not in listed[False]
        assert item_id in listed[True]

        updated = households_meal_plans.update_mealplan(
            mealie_client, item_id=item_id, text=f"{sentinel_name}-note"
        )
        assert updated["endDate"] == (plan_date + span).isoformat()
        assert updated["recipeScale"] == 2.5

        new_date = plan_date + dt.timedelta(days=7)
        moved = households_meal_plans.update_mealplan(
            mealie_client, item_id=item_id, date=new_date.isoformat()
        )
        assert moved["date"] == new_date.isoformat()
        assert moved["endDate"] == (new_date + span).isoformat()
        assert moved["recipeScale"] == 2.5
    finally:
        if item_id is not None:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)


@pytest.mark.live
def test_todays_mealplan_lists_todays_entry(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    # Mealie decides "today" in the server time zone. This process and the
    # server share a clock in CI, so a UTC date matches; a midnight boundary or
    # a server on a different time zone is a known edge.
    today = dt.datetime.now(tz=dt.UTC).date()
    todays_entry = households_meal_plans.create_mealplan(
        mealie_client,
        date=today.isoformat(),
        title=sentinel_name,
        entry_type="dinner",
    )
    other_entry = households_meal_plans.create_mealplan(
        mealie_client,
        date=dt.date(2030, 1, 1).isoformat(),
        title=sentinel_name,
        entry_type="dinner",
    )
    todays_id = todays_entry["id"]
    other_id = other_entry["id"]
    staged = [todays_id, other_id]
    try:
        week_entry = expect_dict(
            "create_mealplan",
            create_one_api_households_mealplans_post.sync_detailed(
                client=mealie_client,
                body=PlanEntryCreate(
                    date=today, end_date=today + dt.timedelta(days=6), title=sentinel_name
                ),
            ),
            HTTPStatus.CREATED,
        )
        staged.append(week_entry["id"])

        entries = call_tool("mealie_get_todays_mealplan", {})
        assert isinstance(entries, list)
        ids = {entry["id"] for entry in entries}
        assert todays_id in ids
        # A dated-elsewhere entry must be filtered out, not returned wholesale.
        assert other_id not in ids
        assert week_entry["id"] not in ids
    finally:
        for item_id in staged:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)


@pytest.mark.live
def test_create_mealplan_round_trips_through_wrapper(
    created_recipe: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    plan_date = dt.date(2030, 1, 2).isoformat()
    created = call_tool(
        "mealie_create_mealplan",
        {
            "date": plan_date,
            "recipe_id": created_recipe["id"],
            "title": sentinel_name,
            "entry_type": "dinner",
        },
    )
    assert isinstance(created, dict)
    item_id = created["id"]
    try:
        assert created["title"] == sentinel_name
        assert created["recipeId"] == created_recipe["id"]
        assert created["date"] == plan_date
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_mealplan", {"item_id": item_id})


@pytest.mark.live
def test_create_mealplan_defaults_to_breakfast_and_scale_one(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
) -> None:
    # With entry_type omitted the key never reaches Mealie, so the server seeds
    # its own slot. The sibling random tool seeds a different one, so pinning
    # this value catches a docstring that names the wrong default.
    plan_date = dt.date(2030, 1, 4).isoformat()
    created = households_meal_plans.create_mealplan(
        mealie_client, date=plan_date, recipe_id=created_recipe["id"]
    )
    item_id = created["id"]
    try:
        assert created["entryType"] == "breakfast"
        assert created["recipeScale"] == 1.0
        fetched = households_meal_plans.get_mealplan(mealie_client, item_id=item_id)
        assert fetched["entryType"] == "breakfast"
    finally:
        with contextlib.suppress(ToolError):
            households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)


@pytest.mark.live
@pytest.mark.usefixtures("created_recipe")
def test_create_random_mealplan_defaults_to_dinner(
    mealie_client: AuthenticatedClient,
) -> None:
    plan_date = dt.date(2030, 1, 5).isoformat()
    created = households_meal_plans.create_random_mealplan(mealie_client, date=plan_date)
    item_id = created["id"]
    try:
        assert created["entryType"] == "dinner"
        fetched = households_meal_plans.get_mealplan(mealie_client, item_id=item_id)
        assert fetched["entryType"] == "dinner"
    finally:
        with contextlib.suppress(ToolError):
            households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)


@pytest.mark.live
@pytest.mark.usefixtures("created_recipe")
def test_create_random_mealplan_fails_when_the_matching_rule_filters_everything_out(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    # A recipe is staged, so an unrestricted pick would succeed. The rule covers
    # this date's weekday and slot and filters on a tag no recipe carries, which
    # narrows the candidate set to nothing. Mealie rejects rather than widening
    # the pick back to the full recipe list.
    plan_date = dt.date(2030, 1, 6)
    rule = households_meal_plan_rules.create_mealplan_rule(
        mealie_client,
        day=plan_date.strftime("%A").lower(),
        entry_type="snack",
        query_filter_string=f'tags.name CONTAINS ALL ["{sentinel_name}"]',
    )
    # Capturing the result means a regression that schedules an entry instead of
    # raising is torn down rather than left on the plan.
    created: dict[str, Any] | None = None
    try:
        with pytest.raises(ToolError, match=r"Mealie create_random_mealplan failed \(404"):
            created = households_meal_plans.create_random_mealplan(
                mealie_client, date=plan_date.isoformat(), entry_type="snack"
            )
    finally:
        if created is not None:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=created["id"])
        with contextlib.suppress(ToolError):
            households_meal_plan_rules.delete_mealplan_rule(mealie_client, item_id=rule["id"])


@pytest.mark.live
@pytest.mark.usefixtures("created_recipe")
def test_create_random_mealplan_picks_a_recipe_for_a_week(
    mealie_client: AuthenticatedClient,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    # A sentinel recipe is staged, so the household holds at least one recipe the
    # server-side random pick can resolve to a real recipe link rather than a null
    # slot. This asserts the pick landed on a recipe, not that it landed on this one.
    plan_date = dt.date(2030, 1, 3)
    end_date = (plan_date + dt.timedelta(days=6)).isoformat()
    item_id: int | None = None
    try:
        created = call_tool(
            "mealie_create_random_mealplan",
            {"date": plan_date.isoformat(), "entry_type": "dinner", "end_date": end_date},
        )
        assert isinstance(created, dict)
        item_id = created["id"]
        assert created["date"] == plan_date.isoformat()
        assert created["endDate"] == end_date
        assert created["entryType"] == "dinner"
        assert created["recipeId"] is not None
    finally:
        if item_id is not None:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)


@pytest.mark.live
def test_create_tools_reject_an_off_span_end_date_and_a_non_positive_scale(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
) -> None:
    # Capturing each result means a regression that schedules an entry instead
    # of raising is torn down rather than left on the plan.
    plan_date = dt.date(2030, 1, 8)
    off_span = (plan_date + dt.timedelta(days=3)).isoformat()
    created: list[dict[str, Any]] = []
    try:
        with pytest.raises(ToolError, match=r"Mealie create_mealplan failed \(422"):
            created.append(
                households_meal_plans.create_mealplan(
                    mealie_client,
                    date=plan_date.isoformat(),
                    end_date=off_span,
                    title=sentinel_name,
                )
            )
        with pytest.raises(ToolError, match=r"Mealie create_random_mealplan failed \(422"):
            created.append(
                households_meal_plans.create_random_mealplan(
                    mealie_client, date=plan_date.isoformat(), end_date=off_span
                )
            )
        with pytest.raises(ToolError, match=r"Mealie create_mealplan failed \(422"):
            created.append(
                households_meal_plans.create_mealplan(
                    mealie_client,
                    date=plan_date.isoformat(),
                    recipe_id=created_recipe["id"],
                    recipe_scale=0,
                )
            )
    finally:
        for entry in created:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=entry["id"])


@pytest.mark.live
def test_update_mealplan_swaps_and_removes_the_recipe_scale_and_week(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """Recipe, scale and week change through the wrapper; empty strings remove them."""
    plan_date = dt.date(2030, 1, 9)
    week_end = (plan_date + dt.timedelta(days=6)).isoformat()
    item_id: int | None = None
    other_slug: str | None = None
    try:
        other_slug = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-other")["slug"]
        other_id = recipe_crud.get_recipe(mealie_client, slug_or_id=other_slug)["id"]
        item_id = households_meal_plans.create_mealplan(
            mealie_client,
            date=plan_date.isoformat(),
            recipe_id=created_recipe["id"],
            recipe_scale=2,
            title=sentinel_name,
            entry_type="lunch",
        )["id"]

        changed = call_tool(
            "mealie_update_mealplan",
            {
                "item_id": item_id,
                "recipe_id": other_id,
                "recipe_scale": 3.5,
                "end_date": week_end,
            },
        )
        assert isinstance(changed, dict)
        assert changed["recipeId"] == other_id
        assert changed["recipeScale"] == 3.5
        assert changed["endDate"] == week_end
        assert changed["title"] == sentinel_name
        assert changed["entryType"] == "lunch"

        with pytest.raises(ToolError, match=r"Mealie update_mealplan failed \(422"):
            households_meal_plans.update_mealplan(
                mealie_client,
                item_id=item_id,
                end_date=(plan_date + dt.timedelta(days=2)).isoformat(),
            )
        with pytest.raises(ToolError, match=r"Mealie update_mealplan failed \(422"):
            households_meal_plans.update_mealplan(mealie_client, item_id=item_id, recipe_scale=0)

        cleared = households_meal_plans.update_mealplan(
            mealie_client, item_id=item_id, recipe_id="", end_date=""
        )
        assert cleared["recipeId"] is None
        assert cleared["endDate"] is None
        assert cleared["date"] == plan_date.isoformat()
        assert cleared["recipeScale"] == 3.5
    finally:
        if item_id is not None:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)
        if other_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=other_slug)


@pytest.mark.live
@pytest.mark.usefixtures("created_recipe")
def test_create_random_mealplan_week_entry_follows_only_all_days_rules(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    # Both rules filter on a tag no recipe carries, so whichever rule applies
    # leaves nothing to pick. The weekday rule blocks a day entry but not a week
    # entry starting that day; the all-days rule blocks the week entry.
    plan_date = dt.date(2030, 1, 13)
    week_end = (plan_date + dt.timedelta(days=6)).isoformat()
    no_match = f'tags.name CONTAINS ALL ["{sentinel_name}"]'
    rule_ids: list[str] = []
    created: list[dict[str, Any]] = []
    try:
        rule_ids.append(
            households_meal_plan_rules.create_mealplan_rule(
                mealie_client,
                day=plan_date.strftime("%A").lower(),
                entry_type="side",
                query_filter_string=no_match,
            )["id"]
        )
        with pytest.raises(ToolError, match=r"Mealie create_random_mealplan failed \(404"):
            created.append(
                households_meal_plans.create_random_mealplan(
                    mealie_client, date=plan_date.isoformat(), entry_type="side"
                )
            )
        week_entry = households_meal_plans.create_random_mealplan(
            mealie_client, date=plan_date.isoformat(), entry_type="side", end_date=week_end
        )
        created.append(week_entry)
        assert week_entry["endDate"] == week_end
        assert week_entry["recipeId"] is not None

        rule_ids.append(
            households_meal_plan_rules.create_mealplan_rule(
                mealie_client, entry_type="side", query_filter_string=no_match
            )["id"]
        )
        with pytest.raises(ToolError, match=r"Mealie create_random_mealplan failed \(404"):
            created.append(
                households_meal_plans.create_random_mealplan(
                    mealie_client, date=plan_date.isoformat(), entry_type="side", end_date=week_end
                )
            )
    finally:
        for entry in created:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=entry["id"])
        for rule_id in rule_ids:
            with contextlib.suppress(ToolError):
                households_meal_plan_rules.delete_mealplan_rule(mealie_client, item_id=rule_id)


@pytest.mark.live
def test_update_mealplan_removes_the_recipe_only_with_a_title(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
) -> None:
    plan_date = dt.date(2030, 1, 10)
    item_id: int | None = None
    try:
        item_id = households_meal_plans.create_mealplan(
            mealie_client, date=plan_date.isoformat(), recipe_id=created_recipe["id"]
        )["id"]

        with pytest.raises(ToolError, match=r"Mealie update_mealplan failed \(422"):
            households_meal_plans.update_mealplan(mealie_client, item_id=item_id, recipe_id="")
        assert (
            households_meal_plans.get_mealplan(mealie_client, item_id=item_id)["recipeId"]
            == created_recipe["id"]
        )

        cleared = households_meal_plans.update_mealplan(
            mealie_client, item_id=item_id, recipe_id="", title=sentinel_name
        )
        assert cleared["recipeId"] is None
        assert cleared["title"] == sentinel_name
    finally:
        if item_id is not None:
            with contextlib.suppress(ToolError):
                households_meal_plans.delete_mealplan(mealie_client, item_id=item_id)
