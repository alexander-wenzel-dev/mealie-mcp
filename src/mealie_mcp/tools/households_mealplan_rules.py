"""Household meal plan rule tools.

Mirrors `mealie_mcp.client.api.households_mealplan_rules`. Exposes CRUD for the
rules that bias Mealie's random meal selection: for a given day and entry type, a
rule constrains the pick with an opaque filter DSL. A rule with ``day`` or
``entry_type`` left as ``unset`` applies to any day or any type. The rule logic
lives entirely in Mealie; these tools are thin CRUD. Like a cookbook, a rule
stores its filter as an opaque ``queryFilterString`` that the create and update
tools pass straight through rather than building from structured category, tag,
or tool inputs.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_mealplan_rules import (
    create_one_api_households_mealplans_rules_post,
    delete_one_api_households_mealplans_rules_item_id_delete,
    get_all_api_households_mealplans_rules_get,
    get_one_api_households_mealplans_rules_item_id_get,
    update_one_api_households_mealplans_rules_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.plan_rules_create import PlanRulesCreate
from mealie_mcp.client.models.plan_rules_day import PlanRulesDay
from mealie_mcp.client.models.plan_rules_type import PlanRulesType
from mealie_mcp.client.types import UNSET, Unset
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_non_empty,
    require_pagination,
    to_unset,
)


def _parse_day(value: str | None) -> PlanRulesDay | Unset:
    """Coerce a caller-supplied day string into the typed enum or UNSET."""
    if value is None:
        return UNSET
    try:
        return PlanRulesDay(value)
    except ValueError as exc:
        allowed = ", ".join(d.value for d in PlanRulesDay)
        raise ToolError(f"day must be one of: {allowed}") from exc


def _parse_rule_type(value: str | None) -> PlanRulesType | Unset:
    """Coerce a caller-supplied entry type string into the typed enum or UNSET."""
    if value is None:
        return UNSET
    try:
        return PlanRulesType(value)
    except ValueError as exc:
        allowed = ", ".join(t.value for t in PlanRulesType)
        raise ToolError(f"entry_type must be one of: {allowed}") from exc


def list_mealplan_rules(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List the household's meal plan rules, paginated. Returns the envelope."""
    require_pagination(page, per_page)
    response = get_all_api_households_mealplans_rules_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_mealplan_rules", response)


def create_mealplan_rule(
    client: AuthenticatedClient,
    day: str | None = None,
    entry_type: str | None = None,
    query_filter_string: str | None = None,
) -> dict[str, Any]:
    """Create a meal plan rule. Returns the new rule payload.

    ``day`` and ``entry_type`` left unset apply the rule to any day or any type.
    ``query_filter_string`` is the opaque Mealie filter DSL that constrains the
    random pick. It is stored verbatim and parsed server-side.
    """
    body = PlanRulesCreate(
        day=_parse_day(day),
        entry_type=_parse_rule_type(entry_type),
        query_filter_string=to_unset(query_filter_string),
    )
    response = create_one_api_households_mealplans_rules_post.sync_detailed(
        client=client, body=body
    )
    return expect_dict("create_mealplan_rule", response, HTTPStatus.CREATED)


def get_mealplan_rule(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a meal plan rule by id. Returns the rule payload."""
    require_non_empty("item_id", item_id)
    response = get_one_api_households_mealplans_rules_item_id_get.sync_detailed(
        item_id, client=client
    )
    return expect_dict("get_mealplan_rule", response)


def update_mealplan_rule(
    client: AuthenticatedClient,
    item_id: str,
    day: str | None = None,
    entry_type: str | None = None,
    query_filter_string: str | None = None,
) -> dict[str, Any]:
    """Edit a rule's day, entry type, or filter. Returns the updated payload.

    Mealie's PUT replaces the resource rather than patching it, so fields absent
    from the request body reset to their schema defaults. The current rule is
    fetched and the merged payload is sent so the fields the caller omits
    survive untouched. The prefetch is routed through
    ``expect_dict("update_mealplan_rule", ...)`` so any failure surfaces under
    the caller's tool name.
    """
    require_non_empty("item_id", item_id)
    if day is None and entry_type is None and query_filter_string is None:
        raise ToolError("update_mealplan_rule requires at least one field to update")
    new_day = _parse_day(day)
    new_entry_type = _parse_rule_type(entry_type)

    prefetch = get_one_api_households_mealplans_rules_item_id_get.sync_detailed(
        item_id, client=client
    )
    existing = expect_dict("update_mealplan_rule", prefetch)
    body = PlanRulesCreate.from_dict(existing)
    body.additional_properties = {}
    if day is not None:
        body.day = new_day
    if entry_type is not None:
        body.entry_type = new_entry_type
    if query_filter_string is not None:
        body.query_filter_string = query_filter_string

    response = update_one_api_households_mealplans_rules_item_id_put.sync_detailed(
        item_id, client=client, body=body
    )
    return expect_dict("update_mealplan_rule", response)


def delete_mealplan_rule(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a meal plan rule by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)
    response = delete_one_api_households_mealplans_rules_item_id_delete.sync_detailed(
        item_id, client=client
    )
    return ack_delete("delete_mealplan_rule", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the household meal plan rule tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_mealplan_rules")
    def _list_mealplan_rules(
        page: int = 1,
        per_page: int = 50,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List the household's meal plan rules, paginated.

        A rule biases Mealie's random meal selection for a given day and entry
        type. Pass a rule to no tool here; rules take effect automatically when
        ``mealie_create_random_mealplan`` picks a recipe.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            order_by: Optional column name to sort on (e.g. ``"day"``).
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_mealplan_rules(
            get_client(),
            page=page,
            per_page=per_page,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_create_mealplan_rule")
    def _create_mealplan_rule(
        day: str | None = None,
        entry_type: str | None = None,
        query_filter_string: str | None = None,
    ) -> dict[str, Any]:
        """Create a meal plan rule that biases Mealie's random meal selection.

        A rule constrains the recipe ``mealie_create_random_mealplan`` picks for
        a matching day and entry type. Leaving ``day`` or ``entry_type`` unset
        applies the rule to any day or any type.

        Args:
            day: Optional day the rule applies to. One of ``monday``,
                ``tuesday``, ``wednesday``, ``thursday``, ``friday``,
                ``saturday``, ``sunday``, or ``unset`` for any day. Defaults to
                any day.
            entry_type: Optional meal slot the rule applies to. One of
                ``breakfast``, ``lunch``, ``dinner``, ``side``, ``snack``,
                ``dessert``, ``drink``, or ``unset`` for any type. Defaults to
                any type.
            query_filter_string: Optional Mealie filter DSL that constrains the
                random pick (e.g. ``'tags.name CONTAINS ALL ["Quick"]'``).
                Stored verbatim and parsed server-side.

        Returns:
            The newly created rule payload as a JSON-compatible dict.
        """
        return create_mealplan_rule(
            get_client(),
            day=day,
            entry_type=entry_type,
            query_filter_string=query_filter_string,
        )

    @mcp.tool(name="mealie_get_mealplan_rule")
    def _get_mealplan_rule(item_id: str) -> dict[str, Any]:
        """Fetch a single meal plan rule by id.

        Args:
            item_id: UUID of the rule.

        Returns:
            The rule payload as a JSON-compatible dict.
        """
        return get_mealplan_rule(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_update_mealplan_rule")
    def _update_mealplan_rule(
        item_id: str,
        day: str | None = None,
        entry_type: str | None = None,
        query_filter_string: str | None = None,
    ) -> dict[str, Any]:
        """Edit an existing meal plan rule.

        Only the supplied fields change; any field left unset keeps its current
        value. At least one field beyond ``item_id`` must be provided.

        Args:
            item_id: UUID of the rule to update.
            day: Optional new day. One of ``monday``, ``tuesday``,
                ``wednesday``, ``thursday``, ``friday``, ``saturday``,
                ``sunday``, or ``unset`` for any day.
            entry_type: Optional new meal slot. One of ``breakfast``, ``lunch``,
                ``dinner``, ``side``, ``snack``, ``dessert``, ``drink``, or
                ``unset`` for any type.
            query_filter_string: Optional new Mealie filter DSL.

        Returns:
            The updated rule payload as a JSON-compatible dict.
        """
        return update_mealplan_rule(
            get_client(),
            item_id=item_id,
            day=day,
            entry_type=entry_type,
            query_filter_string=query_filter_string,
        )

    @mcp.tool(name="mealie_delete_mealplan_rule")
    def _delete_mealplan_rule(item_id: str) -> dict[str, Any]:
        """Delete a meal plan rule from Mealie by id.

        Args:
            item_id: UUID of the rule to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_mealplan_rule(get_client(), item_id=item_id)
