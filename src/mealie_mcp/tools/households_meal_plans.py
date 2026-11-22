"""Household meal plan tools.

Mirrors `mealie_mcp.client.api.households_meal_plans`. Exposes the per-entry
lifecycle: list (paginated, date-range filtered), create, get, update, and
delete, plus a read of today's plan and a server-picked random entry. Meal plan
rules and the shopping helper are out of scope.
"""

from __future__ import annotations

import datetime as dt
from http import HTTPStatus
from typing import Any, Literal
from uuid import UUID

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_meal_plans import (
    create_one_api_households_mealplans_post,
    create_random_meal_api_households_mealplans_random_post,
    delete_one_api_households_mealplans_item_id_delete,
    get_all_api_households_mealplans_get,
    get_one_api_households_mealplans_item_id_get,
    get_todays_meals_api_households_mealplans_today_get,
    update_one_api_households_mealplans_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.plan_entry_create import PlanEntryCreate
from mealie_mcp.client.models.plan_entry_type import PlanEntryType
from mealie_mcp.client.models.plan_entry_update import PlanEntryUpdate
from mealie_mcp.client.models.random_plan_entry_create import RandomPlanEntryCreate
from mealie_mcp.client.types import UNSET, Unset
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    expect_list,
    parse_order_direction,
    parse_uuid,
    require_pagination,
    to_unset,
)


def _parse_date(name: str, value: str) -> dt.date:
    """Parse a required ISO 8601 date string or raise `ToolError`."""
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ToolError(f"{name} must be an ISO 8601 date (YYYY-MM-DD): {exc}") from exc


def _parse_date_opt(name: str, value: str | None) -> dt.date | Unset:
    """Parse an optional ISO 8601 date string into a date or UNSET."""
    if value is None:
        return UNSET
    return _parse_date(name, value)


def _parse_entry_type(value: str | None) -> PlanEntryType | Unset:
    """Coerce a caller-supplied meal type string into the typed enum."""
    if value is None:
        return UNSET
    try:
        return PlanEntryType(value)
    except ValueError as exc:
        allowed = ", ".join(t.value for t in PlanEntryType)
        raise ToolError(f"entry_type must be one of: {allowed}") from exc


def _parse_recipe_id(value: str | None) -> UUID | Unset:
    """Parse an optional recipe UUID string into a UUID or UNSET."""
    if value is None:
        return UNSET
    return parse_uuid("recipe_id", value)


def list_mealplans(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    start_date: str | None = None,
    end_date: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
    include_week_entries: bool = False,
) -> dict[str, Any]:
    """List meal plan entries, paginated and optionally date-range filtered."""
    require_pagination(page, per_page)
    response = get_all_api_households_mealplans_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        start_date=_parse_date_opt("start_date", start_date),
        end_date=_parse_date_opt("end_date", end_date),
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
        include_week_entries=include_week_entries,
    )
    return expect_dict("list_mealplans", response)


def todays_mealplan(client: AuthenticatedClient) -> list[dict[str, Any]]:
    """Return today's meal plan entries. Mealie decides "today" server-side."""
    response = get_todays_meals_api_households_mealplans_today_get.sync_detailed(client=client)
    return expect_list("todays_mealplan", response)


def create_mealplan(
    client: AuthenticatedClient,
    date: str,
    recipe_id: str | None = None,
    title: str | None = None,
    text: str | None = None,
    entry_type: str | None = None,
    end_date: str | None = None,
    recipe_scale: float | None = None,
) -> dict[str, Any]:
    """Create a meal plan entry. Returns the new entry payload."""
    body = PlanEntryCreate(
        date=_parse_date("date", date),
        end_date=_parse_date_opt("end_date", end_date),
        recipe_id=_parse_recipe_id(recipe_id),
        recipe_scale=to_unset(recipe_scale),
        title=to_unset(title),
        text=to_unset(text),
        entry_type=_parse_entry_type(entry_type),
    )
    response = create_one_api_households_mealplans_post.sync_detailed(client=client, body=body)
    return expect_dict("create_mealplan", response, HTTPStatus.CREATED)


def create_random_mealplan(
    client: AuthenticatedClient,
    date: str,
    entry_type: str | None = None,
    end_date: str | None = None,
) -> dict[str, Any]:
    """Create a meal plan entry with a recipe Mealie picks at random.

    Mealie selects the recipe server-side, honouring the household's meal plan
    rules. Returns the created entry payload.
    """
    body = RandomPlanEntryCreate(
        date=_parse_date("date", date),
        end_date=_parse_date_opt("end_date", end_date),
        entry_type=_parse_entry_type(entry_type),
    )
    response = create_random_meal_api_households_mealplans_random_post.sync_detailed(
        client=client, body=body
    )
    return expect_dict("create_random_mealplan", response)


def get_mealplan(client: AuthenticatedClient, item_id: int) -> dict[str, Any]:
    """Fetch a meal plan entry by id. Returns the entry payload."""
    response = get_one_api_households_mealplans_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_mealplan", response)


def update_mealplan(
    client: AuthenticatedClient,
    item_id: int,
    *,
    date: str | None = None,
    title: str | None = None,
    text: str | None = None,
    entry_type: str | None = None,
    recipe_id: str | None = None,
    recipe_scale: float | None = None,
    end_date: str | None = None,
) -> dict[str, Any]:
    """Update a meal plan entry. Returns the updated entry payload.

    The endpoint PUT-replaces the entry, so the current entry is fetched and
    the caller's edits are merged onto it. Fields left unset keep their current
    value. A new ``date`` without ``end_date`` moves the week span with it. An
    empty ``recipe_id`` removes the recipe link and an empty ``end_date`` makes
    the entry a single day.
    """
    supplied = (date, title, text, entry_type, recipe_id, recipe_scale, end_date)
    if all(value is None for value in supplied):
        raise ToolError("update_mealplan requires at least one field to update")

    new_date = _parse_date("date", date) if date is not None else None
    new_entry_type = _parse_entry_type(entry_type)
    new_recipe_id = parse_uuid("recipe_id", recipe_id) if recipe_id else None
    new_end_date = _parse_date("end_date", end_date) if end_date else None

    current = get_mealplan(client, item_id)
    current_recipe_id = current.get("recipeId")
    current_date = _parse_date("date", current["date"])
    plan_date = new_date if new_date is not None else current_date
    current_end_date = current.get("endDate")
    if end_date is not None:
        plan_end_date = new_end_date
    elif current_end_date:
        plan_end_date = plan_date + (_parse_date("endDate", current_end_date) - current_date)
    else:
        plan_end_date = None
    if recipe_id is not None:
        plan_recipe_id = new_recipe_id
    else:
        plan_recipe_id = UUID(current_recipe_id) if current_recipe_id else None
    body = PlanEntryUpdate(
        id=item_id,
        group_id=UUID(current["groupId"]),
        user_id=UUID(current["userId"]),
        date=plan_date,
        end_date=plan_end_date,
        title=to_unset(title if title is not None else current.get("title")),
        text=to_unset(text if text is not None else current.get("text")),
        entry_type=(
            new_entry_type
            if entry_type is not None
            else _parse_entry_type(current.get("entryType"))
        ),
        recipe_id=plan_recipe_id,
        recipe_scale=to_unset(
            recipe_scale if recipe_scale is not None else current.get("recipeScale")
        ),
    )
    response = update_one_api_households_mealplans_item_id_put.sync_detailed(
        item_id, client=client, body=body
    )
    return expect_dict("update_mealplan", response)


def delete_mealplan(client: AuthenticatedClient, item_id: int) -> dict[str, Any]:
    """Delete a meal plan entry by id. Returns ``{"id": str(item_id), "deleted": True}``."""
    response = delete_one_api_households_mealplans_item_id_delete.sync_detailed(
        item_id, client=client
    )
    return ack_delete("delete_mealplan", response, str(item_id))


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the household meal plan tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_mealplans")
    def _list_mealplans(
        page: int = 1,
        per_page: int = 50,
        start_date: str | None = None,
        end_date: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
        include_week_entries: bool = False,
    ) -> dict[str, Any]:
        """List meal plan entries for the household, paginated.

        Entries planned for a whole week rather than a day are left out unless
        ``include_week_entries`` is true. A week entry matches the date range
        when its week overlaps it.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            start_date: Optional inclusive lower bound as ``YYYY-MM-DD``.
            end_date: Optional inclusive upper bound as ``YYYY-MM-DD``.
            order_by: Optional column name to sort on (e.g. ``"date"``).
            order_direction: ``"asc"`` or ``"desc"``.
            include_week_entries: Also list week entries. Defaults to false.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_mealplans(
            get_client(),
            page=page,
            per_page=per_page,
            start_date=start_date,
            end_date=end_date,
            order_by=order_by,
            order_direction=order_direction,
            include_week_entries=include_week_entries,
        )

    @mcp.tool(name="mealie_get_todays_mealplan")
    def _get_todays_mealplan() -> list[dict[str, Any]]:
        """List the meal plan entries scheduled for today.

        Mealie determines "today" server-side, so the caller supplies no date
        and needs no knowledge of the server time zone. Entries planned for a
        whole week are not included. An empty plan returns an empty list, not
        an error.

        Returns:
            A list of today's meal plan entries. The MCP structured output wraps
            the list under a ``result`` key (``{"result": [...]}``).
        """
        return todays_mealplan(get_client())

    @mcp.tool(name="mealie_create_mealplan")
    def _create_mealplan(
        date: str,
        recipe_id: str | None = None,
        title: str | None = None,
        text: str | None = None,
        entry_type: str | None = None,
        end_date: str | None = None,
        recipe_scale: float | None = None,
    ) -> dict[str, Any]:
        """Create a meal plan entry for a single day or a whole week.

        An entry references either a recipe (via ``recipe_id``) or a free-text
        ``title``/``text`` note. Mealie references recipes by UUID here, not by
        slug. A week entry needs ``end_date`` exactly six days after ``date``;
        Mealie rejects any other end date with a 422.

        Args:
            date: Day of the entry as ``YYYY-MM-DD``. Required.
            recipe_id: Optional recipe UUID to schedule.
            title: Optional free-text title for a non-recipe entry.
            text: Optional free-text note.
            entry_type: Meal slot. One of ``breakfast``, ``lunch``, ``dinner``,
                ``side``, ``snack``, ``dessert``, ``drink``. If omitted, Mealie
                seeds ``breakfast``; ``mealie_create_random_mealplan`` seeds
                ``dinner`` instead.
            end_date: Optional last day of a week entry as ``YYYY-MM-DD``,
                exactly six days after ``date``. Omit for a single day.
            recipe_scale: Optional multiplier for the recipe's servings,
                greater than 0. Mealie stores 1 when omitted and rejects 0 or
                less with a 422.

        Returns:
            The newly created meal plan entry as a JSON-compatible dict.
        """
        return create_mealplan(
            get_client(),
            date=date,
            recipe_id=recipe_id,
            title=title,
            text=text,
            entry_type=entry_type,
            end_date=end_date,
            recipe_scale=recipe_scale,
        )

    @mcp.tool(name="mealie_create_random_mealplan")
    def _create_random_mealplan(
        date: str,
        entry_type: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """Add a meal plan entry whose recipe Mealie picks at random.

        Mealie chooses the recipe server-side from the household's recipes,
        following any meal plan rules the household has configured. Use this to
        fill a slot without naming a recipe. The household must have at least one
        recipe for the pick to succeed. If a rule covers the day and slot but its
        filter matches no recipe, the call fails with a 404 instead of falling
        back to the unfiltered list. A week entry needs ``end_date`` exactly six
        days after ``date``; Mealie rejects any other end date with a 422.

        Args:
            date: Day of the entry as ``YYYY-MM-DD``. Required.
            entry_type: Meal slot. One of ``breakfast``, ``lunch``, ``dinner``,
                ``side``, ``snack``, ``dessert``, ``drink``. If omitted, Mealie
                seeds ``dinner``; ``mealie_create_mealplan`` seeds ``breakfast``
                instead.
            end_date: Optional last day of a week entry as ``YYYY-MM-DD``,
                exactly six days after ``date``. Omit for a single day.

        Returns:
            The newly created meal plan entry as a JSON-compatible dict.
        """
        return create_random_mealplan(
            get_client(),
            date=date,
            entry_type=entry_type,
            end_date=end_date,
        )

    @mcp.tool(name="mealie_get_mealplan")
    def _get_mealplan(item_id: int) -> dict[str, Any]:
        """Fetch a single meal plan entry by id.

        Args:
            item_id: Integer id of the meal plan entry.

        Returns:
            The meal plan entry payload as a JSON-compatible dict.
        """
        return get_mealplan(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_update_mealplan")
    def _update_mealplan(
        item_id: int,
        date: str | None = None,
        title: str | None = None,
        text: str | None = None,
        entry_type: str | None = None,
        recipe_id: str | None = None,
        recipe_scale: float | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        """Edit fields on an existing meal plan entry.

        Only the fields supplied are changed; omitted fields keep their current
        value. A week entry keeps its week, and a new ``date`` without
        ``end_date`` moves the week to start on that day. At least one field
        beyond ``item_id`` must be provided.

        Args:
            item_id: Integer id of the meal plan entry.
            date: New day as ``YYYY-MM-DD``.
            title: New free-text title.
            text: New free-text note.
            entry_type: New meal slot. One of ``breakfast``, ``lunch``,
                ``dinner``, ``side``, ``snack``, ``dessert``, ``drink``.
            recipe_id: New recipe UUID, or an empty string to remove the
                recipe link.
            recipe_scale: New multiplier for the recipe's servings, greater
                than 0. Mealie rejects 0 or less with a 422.
            end_date: ``YYYY-MM-DD`` exactly six days after the entry's date to
                make it a week entry, or an empty string to make it a single
                day. Mealie rejects any other end date with a 422.

        Returns:
            The updated meal plan entry payload as a JSON-compatible dict.
        """
        return update_mealplan(
            get_client(),
            item_id=item_id,
            date=date,
            title=title,
            text=text,
            entry_type=entry_type,
            recipe_id=recipe_id,
            recipe_scale=recipe_scale,
            end_date=end_date,
        )

    @mcp.tool(name="mealie_delete_mealplan")
    def _delete_mealplan(item_id: int) -> dict[str, Any]:
        """Delete a meal plan entry from Mealie by id.

        Args:
            item_id: Integer id of the meal plan entry to delete.

        Returns:
            A canonical acknowledgement ``{"id": str(<item_id>), "deleted": True}``.
        """
        return delete_mealplan(get_client(), item_id=item_id)
