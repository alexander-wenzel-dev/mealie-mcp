"""Household meal plan tools.

Mirrors `mealie_mcp.client.api.households_mealplans`. Exposes the per-entry
lifecycle: list (paginated, date-range filtered), create, get, update, and
delete. Meal plan rules, random-meal generation, and the today/shopping
helpers are out of scope.
"""

from __future__ import annotations

import datetime as dt
from http import HTTPStatus
from typing import Any, Literal
from uuid import UUID

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_mealplans import (
    create_one_api_households_mealplans_post,
    delete_one_api_households_mealplans_item_id_delete,
    get_all_api_households_mealplans_get,
    get_one_api_households_mealplans_item_id_get,
    update_one_api_households_mealplans_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_plan_entry import CreatePlanEntry
from mealie_mcp.client.models.plan_entry_type import PlanEntryType
from mealie_mcp.client.models.update_plan_entry import UpdatePlanEntry
from mealie_mcp.client.types import UNSET, Unset
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_per_page,
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
    try:
        return UUID(value)
    except ValueError as exc:
        raise ToolError(f"recipe_id must be a recipe UUID: {exc}") from exc


def list_mealplans(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    start_date: str | None = None,
    end_date: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List meal plan entries, paginated and optionally date-range filtered."""
    require_per_page(per_page)
    response = get_all_api_households_mealplans_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        start_date=_parse_date_opt("start_date", start_date),
        end_date=_parse_date_opt("end_date", end_date),
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_mealplans", response)


def create_mealplan(
    client: AuthenticatedClient,
    date: str,
    recipe_id: str | None = None,
    title: str | None = None,
    text: str | None = None,
    entry_type: str | None = None,
) -> dict[str, Any]:
    """Create a meal plan entry. Returns the new entry payload."""
    body = CreatePlanEntry(
        date=_parse_date("date", date),
        recipe_id=_parse_recipe_id(recipe_id),
        title=to_unset(title),
        text=to_unset(text),
        entry_type=_parse_entry_type(entry_type),
    )
    response = create_one_api_households_mealplans_post.sync_detailed(client=client, body=body)
    return expect_dict("create_mealplan", response, HTTPStatus.CREATED)


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
) -> dict[str, Any]:
    """Update a meal plan entry. Returns the updated entry payload.

    The endpoint PUT-replaces the entry, so the current entry is fetched and
    the caller's edits are merged onto it. Fields left unset keep their current
    value, and the entry's recipe link is preserved.
    """
    if date is None and title is None and text is None and entry_type is None:
        raise ToolError("update_mealplan requires at least one field to update")

    new_date = _parse_date("date", date) if date is not None else None
    new_entry_type = _parse_entry_type(entry_type)

    current = get_mealplan(client, item_id)
    current_recipe_id = current.get("recipeId")
    body = UpdatePlanEntry(
        id=item_id,
        group_id=UUID(current["groupId"]),
        user_id=UUID(current["userId"]),
        date=new_date if new_date is not None else _parse_date("date", current["date"]),
        title=to_unset(title if title is not None else current.get("title")),
        text=to_unset(text if text is not None else current.get("text")),
        entry_type=(
            new_entry_type
            if entry_type is not None
            else _parse_entry_type(current.get("entryType"))
        ),
        recipe_id=UUID(current_recipe_id) if current_recipe_id else None,
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
    ) -> dict[str, Any]:
        """List meal plan entries for the household, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50. Capped at 100.
            start_date: Optional inclusive lower bound as ``YYYY-MM-DD``.
            end_date: Optional inclusive upper bound as ``YYYY-MM-DD``.
            order_by: Optional column name to sort on (e.g. ``"date"``).
            order_direction: ``"asc"`` or ``"desc"``.

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
        )

    @mcp.tool(name="mealie_create_mealplan")
    def _create_mealplan(
        date: str,
        recipe_id: str | None = None,
        title: str | None = None,
        text: str | None = None,
        entry_type: str | None = None,
    ) -> dict[str, Any]:
        """Create a meal plan entry for a single day.

        An entry references either a recipe (via ``recipe_id``) or a free-text
        ``title``/``text`` note. Mealie references recipes by UUID here, not by
        slug.

        Args:
            date: Day of the entry as ``YYYY-MM-DD``. Required.
            recipe_id: Optional recipe UUID to schedule.
            title: Optional free-text title for a non-recipe entry.
            text: Optional free-text note.
            entry_type: Optional meal slot. One of ``breakfast``, ``lunch``,
                ``dinner``, ``side``, ``snack``, ``dessert``, ``drink``.

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
    ) -> dict[str, Any]:
        """Edit fields on an existing meal plan entry.

        Only the fields supplied are changed; omitted fields keep their current
        value and the entry's recipe link is preserved. At least one field
        beyond ``item_id`` must be provided. The recipe link is read-only
        through this tool; change it by deleting the entry and creating a new
        one with the desired ``recipe_id``.

        Args:
            item_id: Integer id of the meal plan entry.
            date: New day as ``YYYY-MM-DD``.
            title: New free-text title.
            text: New free-text note.
            entry_type: New meal slot. One of ``breakfast``, ``lunch``,
                ``dinner``, ``side``, ``snack``, ``dessert``, ``drink``.

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
