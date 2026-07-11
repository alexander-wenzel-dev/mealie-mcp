"""Recipe unit tools.

Mirrors `mealie_mcp.client.api.recipes_units`. Exposes list, read, create,
update, and delete for ingredient units.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipes_units import (
    create_one_api_units_post,
    delete_one_api_units_item_id_delete,
    get_all_api_units_get,
    get_one_api_units_item_id_get,
    update_one_api_units_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_unit import CreateIngredientUnit
from mealie_mcp.client.models.create_ingredient_unit_alias import CreateIngredientUnitAlias
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_non_empty,
    require_pagination,
    to_unset,
)


def list_units(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List ingredient units, paginated. Returns the pagination envelope."""
    require_pagination(page, per_page)
    response = get_all_api_units_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=to_unset(search),
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_units", response)


def get_unit(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Fetch a unit by id. Returns the unit payload."""
    require_non_empty("item_id", item_id)

    response = get_one_api_units_item_id_get.sync_detailed(item_id, client=client)
    return expect_dict("get_unit", response)


def _alias_bodies(aliases: list[str]) -> list[CreateIngredientUnitAlias]:
    """Translate caller alias names into the generated alias model."""
    for alias in aliases:
        require_non_empty("aliases entry", alias)
    return [CreateIngredientUnitAlias(name=alias) for alias in aliases]


def create_unit(
    client: AuthenticatedClient,
    name: str,
    abbreviation: str | None = None,
    plural_name: str | None = None,
    plural_abbreviation: str | None = None,
    use_abbreviation: bool | None = None,
    fraction: bool | None = None,
    aliases: list[str] | None = None,
) -> dict[str, Any]:
    """Create a unit. Returns the new unit payload."""
    require_non_empty("name", name)

    body = CreateIngredientUnit(
        name=name,
        abbreviation=to_unset(abbreviation),
        plural_name=to_unset(plural_name),
        plural_abbreviation=to_unset(plural_abbreviation),
        use_abbreviation=to_unset(use_abbreviation),
        fraction=to_unset(fraction),
    )
    if aliases is not None:
        body.aliases = _alias_bodies(aliases)

    response = create_one_api_units_post.sync_detailed(client=client, body=body)
    return expect_dict("create_unit", response, HTTPStatus.CREATED)


def update_unit(
    client: AuthenticatedClient,
    item_id: str,
    name: str | None = None,
    abbreviation: str | None = None,
    plural_name: str | None = None,
    plural_abbreviation: str | None = None,
    use_abbreviation: bool | None = None,
    fraction: bool | None = None,
    aliases: list[str] | None = None,
) -> dict[str, Any]:
    """Update fields of an existing unit. Returns the updated unit payload.

    Mealie's PUT replaces the resource rather than patching it, so the current
    unit is fetched and merged with the caller's edits; fields the caller does
    not set survive instead of resetting to their schema defaults.
    """
    require_non_empty("item_id", item_id)
    edits = (
        name,
        abbreviation,
        plural_name,
        plural_abbreviation,
        use_abbreviation,
        fraction,
        aliases,
    )
    if all(edit is None for edit in edits):
        raise ToolError("update_unit requires at least one field to update")
    if name is not None:
        require_non_empty("name", name)
    alias_bodies = _alias_bodies(aliases) if aliases is not None else None

    prefetch = get_one_api_units_item_id_get.sync_detailed(item_id, client=client)
    existing = expect_dict("update_unit", prefetch)
    body = CreateIngredientUnit.from_dict(existing)
    body.additional_properties = {}
    if name is not None:
        body.name = name
    if abbreviation is not None:
        body.abbreviation = abbreviation
    if plural_name is not None:
        body.plural_name = plural_name
    if plural_abbreviation is not None:
        body.plural_abbreviation = plural_abbreviation
    if use_abbreviation is not None:
        body.use_abbreviation = use_abbreviation
    if fraction is not None:
        body.fraction = fraction
    if alias_bodies is not None:
        body.aliases = alias_bodies

    response = update_one_api_units_item_id_put.sync_detailed(item_id, client=client, body=body)
    return expect_dict("update_unit", response)


def delete_unit(client: AuthenticatedClient, item_id: str) -> dict[str, Any]:
    """Delete a unit by id. Returns ``{"id": item_id, "deleted": True}``."""
    require_non_empty("item_id", item_id)

    response = delete_one_api_units_item_id_delete.sync_detailed(item_id, client=client)
    return ack_delete("delete_unit", response, item_id)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the unit tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_units")
    def _list_units(
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List ingredient units from Mealie, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            search: Optional free-text search.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_units(
            get_client(),
            page=page,
            per_page=per_page,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_get_unit")
    def _get_unit(item_id: str) -> dict[str, Any]:
        """Fetch a single unit from Mealie by id.

        Args:
            item_id: UUID of the unit.

        Returns:
            The unit payload as a JSON-compatible dict.
        """
        return get_unit(get_client(), item_id=item_id)

    @mcp.tool(name="mealie_create_unit")
    def _create_unit(
        name: str,
        abbreviation: str | None = None,
        plural_name: str | None = None,
        plural_abbreviation: str | None = None,
        use_abbreviation: bool | None = None,
        fraction: bool | None = None,
        aliases: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create an ingredient unit in Mealie.

        Args:
            name: Human readable unit name. Required, must be non-empty.
            abbreviation: Short form, for example ``tbsp``. Omit to leave unset.
            plural_name: Plural form of the name. Omit to leave unset.
            plural_abbreviation: Plural short form. Omit to leave unset.
            use_abbreviation: Display the abbreviation instead of the name.
            fraction: Display quantities of this unit as fractions.
            aliases: Alternative names the ingredient parser also matches.

        Returns:
            The newly created unit payload as a JSON-compatible dict.
        """
        return create_unit(
            get_client(),
            name=name,
            abbreviation=abbreviation,
            plural_name=plural_name,
            plural_abbreviation=plural_abbreviation,
            use_abbreviation=use_abbreviation,
            fraction=fraction,
            aliases=aliases,
        )

    @mcp.tool(name="mealie_update_unit")
    def _update_unit(
        item_id: str,
        name: str | None = None,
        abbreviation: str | None = None,
        plural_name: str | None = None,
        plural_abbreviation: str | None = None,
        use_abbreviation: bool | None = None,
        fraction: bool | None = None,
        aliases: list[str] | None = None,
    ) -> dict[str, Any]:
        """Update an existing unit in Mealie. Pass at least one field.

        Fields left out keep their current values.

        Args:
            item_id: UUID of the unit to update.
            name: New name. Must be non-empty when given.
            abbreviation: New short form, for example ``tbsp``. Pass an empty
                string to clear it.
            plural_name: New plural form of the name. Pass an empty string to
                clear it.
            plural_abbreviation: New plural short form. Pass an empty string to
                clear it.
            use_abbreviation: Display the abbreviation instead of the name.
            fraction: Display quantities of this unit as fractions.
            aliases: Replacement list of alternative names. Replaces the
                whole list; pass an empty list to clear all aliases.

        Returns:
            The updated unit payload as a JSON-compatible dict.
        """
        return update_unit(
            get_client(),
            item_id=item_id,
            name=name,
            abbreviation=abbreviation,
            plural_name=plural_name,
            plural_abbreviation=plural_abbreviation,
            use_abbreviation=use_abbreviation,
            fraction=fraction,
            aliases=aliases,
        )

    @mcp.tool(name="mealie_delete_unit")
    def _delete_unit(item_id: str) -> dict[str, Any]:
        """Delete a unit from Mealie by id.

        Args:
            item_id: UUID of the unit to delete.

        Returns:
            A canonical acknowledgement ``{"id": <item_id>, "deleted": True}``.
        """
        return delete_unit(get_client(), item_id=item_id)
