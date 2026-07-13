"""Live test for the household meal plan entry lifecycle.

Stages a sentinel recipe, schedules a sentinel meal plan entry that references
it, exercises the get, list, update, and delete tools, then tears both
sentinels down. The update step changes only ``text`` and asserts that the
unsupplied ``recipe_id`` link and ``entry_type`` survive the PUT-replace, so a
regression in fetch-then-merge would fail the test. Cleanup runs even when the
test body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
import datetime as dt
from collections.abc import Callable, Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_mealplans, recipe_crud


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
    created = households_mealplans.create_mealplan(
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
            households_mealplans.delete_mealplan(mealie_client, item_id=item_id)


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

    fetched = households_mealplans.get_mealplan(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["recipeId"] == recipe_id
    assert fetched["title"] == title
    assert fetched["entryType"] == "dinner"

    listing = households_mealplans.list_mealplans(
        mealie_client,
        start_date=plan_date.isoformat(),
        end_date=plan_date.isoformat(),
        per_page=100,
    )
    assert any(entry["id"] == item_id for entry in listing["items"])

    # An entry outside the requested range must not appear.
    other_day = households_mealplans.list_mealplans(
        mealie_client,
        start_date=(plan_date + dt.timedelta(days=1)).isoformat(),
        end_date=(plan_date + dt.timedelta(days=1)).isoformat(),
        per_page=100,
    )
    assert all(entry["id"] != item_id for entry in other_day["items"])

    # Update only the note. The recipe link, title, and entry_type are not
    # supplied, so they must be preserved by fetch-then-merge rather than reset.
    updated = households_mealplans.update_mealplan(mealie_client, item_id=item_id, text=note)
    assert updated["text"] == note
    assert updated["recipeId"] == recipe_id
    assert updated["title"] == title
    assert updated["entryType"] == "dinner"

    # A supplied field changes; the date moves and the recipe link still holds.
    new_date = plan_date + dt.timedelta(days=2)
    moved = households_mealplans.update_mealplan(
        mealie_client, item_id=item_id, date=new_date.isoformat(), entry_type="lunch"
    )
    assert moved["date"] == new_date.isoformat()
    assert moved["entryType"] == "lunch"
    assert moved["text"] == note
    assert moved["recipeId"] == recipe_id

    ack = households_mealplans.delete_mealplan(mealie_client, item_id=item_id)
    assert ack == {"id": str(item_id), "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_mealplan failed \(404"):
        households_mealplans.get_mealplan(mealie_client, item_id=item_id)


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
    todays_entry = households_mealplans.create_mealplan(
        mealie_client,
        date=today.isoformat(),
        title=sentinel_name,
        entry_type="dinner",
    )
    other_entry = households_mealplans.create_mealplan(
        mealie_client,
        date=dt.date(2030, 1, 1).isoformat(),
        title=sentinel_name,
        entry_type="dinner",
    )
    todays_id = todays_entry["id"]
    other_id = other_entry["id"]
    try:
        entries = call_tool("mealie_get_todays_mealplan", {})
        assert isinstance(entries, list)
        ids = {entry["id"] for entry in entries}
        assert todays_id in ids
        # A dated-elsewhere entry must be filtered out, not returned wholesale.
        assert other_id not in ids
    finally:
        for item_id in (todays_id, other_id):
            with contextlib.suppress(ToolError):
                households_mealplans.delete_mealplan(mealie_client, item_id=item_id)


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
@pytest.mark.usefixtures("created_recipe")
def test_create_random_mealplan_picks_a_recipe(
    mealie_client: AuthenticatedClient,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    # A sentinel recipe is staged, so the household holds at least one recipe the
    # server-side random pick can resolve to a real recipe link rather than a null
    # slot. This asserts the pick landed on a recipe, not that it landed on this one.
    plan_date = dt.date(2030, 1, 3).isoformat()
    created = call_tool(
        "mealie_create_random_mealplan",
        {"date": plan_date, "entry_type": "dinner"},
    )
    assert isinstance(created, dict)
    item_id = created["id"]
    try:
        assert created["date"] == plan_date
        assert created["entryType"] == "dinner"
        assert created["recipeId"] is not None
    finally:
        with contextlib.suppress(ToolError):
            households_mealplans.delete_mealplan(mealie_client, item_id=item_id)
