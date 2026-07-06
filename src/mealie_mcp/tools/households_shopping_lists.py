"""Household shopping list tools.

Mirrors `mealie_mcp.client.api.households_shopping_lists`. Exposes the list
lifecycle (list, create, get, rename, delete) and the recipe-to-list bridge that
turns a meal plan into groceries: add one recipe's ingredients, add several in
one call, and remove a recipe's ingredients. Label settings are out of scope;
the items themselves live in `households_shopping_list_items`.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_shopping_lists import (
    add_recipe_ingredients_to_list_api_households_shopping_lists_item_id_recipe_post as add_recipes_endpoint,  # noqa: E501
)
from mealie_mcp.client.api.households_shopping_lists import (
    add_single_recipe_ingredients_to_list_api_households_shopping_lists_item_id_recipe_recipe_id_post as add_recipe_endpoint,  # noqa: E501
)
from mealie_mcp.client.api.households_shopping_lists import (
    create_one_api_households_shopping_lists_post,
    delete_one_api_households_shopping_lists_item_id_delete,
    get_all_api_households_shopping_lists_get,
    get_one_api_households_shopping_lists_item_id_get,
    update_one_api_households_shopping_lists_item_id_put,
)
from mealie_mcp.client.api.households_shopping_lists import (
    remove_recipe_ingredients_from_list_api_households_shopping_lists_item_id_recipe_recipe_id_delete_post as remove_recipe_endpoint,  # noqa: E501
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.shopping_list_add_recipe_params import ShoppingListAddRecipeParams
from mealie_mcp.client.models.shopping_list_add_recipe_params_bulk import (
    ShoppingListAddRecipeParamsBulk,
)
from mealie_mcp.client.models.shopping_list_create import ShoppingListCreate
from mealie_mcp.client.models.shopping_list_remove_recipe_params import (
    ShoppingListRemoveRecipeParams,
)
from mealie_mcp.client.models.shopping_list_update import ShoppingListUpdate
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    parse_order_direction,
    require_non_empty,
    require_pagination,
    to_unset,
)


def list_shopping_lists(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List shopping lists for the household, paginated."""
    require_pagination(page, per_page)
    response = get_all_api_households_shopping_lists_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_shopping_lists", response)


def create_shopping_list(client: AuthenticatedClient, name: str) -> dict[str, Any]:
    """Create a shopping list. Returns the new list payload."""
    require_non_empty("name", name)
    body = ShoppingListCreate(name=name)
    response = create_one_api_households_shopping_lists_post.sync_detailed(client=client, body=body)
    return expect_dict("create_shopping_list", response, HTTPStatus.CREATED)


def get_shopping_list(client: AuthenticatedClient, list_id: str) -> dict[str, Any]:
    """Fetch a shopping list by id, including its items. Returns the list payload."""
    require_non_empty("list_id", list_id)
    response = get_one_api_households_shopping_lists_item_id_get.sync_detailed(
        list_id, client=client
    )
    return expect_dict("get_shopping_list", response)


def update_shopping_list(client: AuthenticatedClient, list_id: str, name: str) -> dict[str, Any]:
    """Rename a shopping list. Returns the updated list payload.

    Mealie's PUT replaces the resource rather than patching it, so fields
    absent from the request body reset to their schema defaults. The current
    list is fetched and the merged payload is sent so untouched items, extras,
    and recipe links survive. The prefetch is routed through
    ``expect_dict("update_shopping_list", ...)`` so any failure surfaces under
    the caller's tool name.
    """
    require_non_empty("list_id", list_id)
    require_non_empty("name", name)

    prefetch = get_one_api_households_shopping_lists_item_id_get.sync_detailed(
        list_id, client=client
    )
    existing = expect_dict("update_shopping_list", prefetch)
    body = ShoppingListUpdate.from_dict(existing)
    body.additional_properties = {}
    body.name = name

    response = update_one_api_households_shopping_lists_item_id_put.sync_detailed(
        list_id, client=client, body=body
    )
    return expect_dict("update_shopping_list", response)


def delete_shopping_list(client: AuthenticatedClient, list_id: str) -> dict[str, Any]:
    """Delete a shopping list by id. Returns ``{"id": list_id, "deleted": True}``."""
    require_non_empty("list_id", list_id)
    response = delete_one_api_households_shopping_lists_item_id_delete.sync_detailed(
        list_id, client=client
    )
    return ack_delete("delete_shopping_list", response, list_id)


def add_recipe_to_shopping_list(
    client: AuthenticatedClient,
    list_id: str,
    recipe_id: str,
    scale: float = 1.0,
) -> dict[str, Any]:
    """Add one recipe's ingredients to a shopping list. Returns the updated list.

    ``scale`` multiplies the ingredient quantities, so ``2.0`` adds a double
    batch. It also lands on the list's recipe reference, where it accumulates
    across repeated adds.
    """
    require_non_empty("list_id", list_id)
    require_non_empty("recipe_id", recipe_id)
    body = ShoppingListAddRecipeParams(recipe_increment_quantity=scale)
    response = add_recipe_endpoint.sync_detailed(list_id, recipe_id, client=client, body=body)
    return expect_dict("add_recipe_to_shopping_list", response)


def add_recipes_to_shopping_list(
    client: AuthenticatedClient,
    list_id: str,
    recipes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Add several recipes' ingredients to a shopping list in one call.

    Each entry of ``recipes`` is an object with a required ``recipe_id`` and an
    optional ``scale`` (default ``1.0``). Returns the updated list.
    """
    require_non_empty("list_id", list_id)
    if not recipes:
        raise ToolError("recipes must be a non-empty list")
    body = [_to_bulk_param(entry) for entry in recipes]
    response = add_recipes_endpoint.sync_detailed(list_id, client=client, body=body)
    return expect_dict("add_recipes_to_shopping_list", response)


def remove_recipe_from_shopping_list(
    client: AuthenticatedClient,
    list_id: str,
    recipe_id: str,
    scale: float = 1.0,
) -> dict[str, Any]:
    """Remove one recipe's ingredients from a shopping list. Returns the updated list.

    ``scale`` decrements the recipe reference by that amount, mirroring
    ``add_recipe_to_shopping_list``. Removing as much as was added drops the
    reference entirely.
    """
    require_non_empty("list_id", list_id)
    require_non_empty("recipe_id", recipe_id)
    body = ShoppingListRemoveRecipeParams(recipe_decrement_quantity=scale)
    response = remove_recipe_endpoint.sync_detailed(list_id, recipe_id, client=client, body=body)
    return expect_dict("remove_recipe_from_shopping_list", response)


def _to_bulk_param(entry: dict[str, Any]) -> ShoppingListAddRecipeParamsBulk:
    """Build one bulk add-recipe param from a caller-supplied entry."""
    if not isinstance(entry, dict):
        raise ToolError("each recipe must be an object with a recipe_id")
    recipe_id = entry.get("recipe_id")
    if not isinstance(recipe_id, str):
        raise ToolError("each recipe must include a recipe_id string")
    require_non_empty("recipe_id", recipe_id)
    scale = entry.get("scale", 1.0)
    if not isinstance(scale, (int, float)):
        raise ToolError("each recipe's scale must be a number")
    return ShoppingListAddRecipeParamsBulk(recipe_id=recipe_id, recipe_increment_quantity=scale)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the household shopping list tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_list_shopping_lists")
    def _list_shopping_lists(
        page: int = 1,
        per_page: int = 50,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List the household's shopping lists, paginated.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size, 1 to 100. Defaults to 50.
            order_by: Optional column name to sort on (e.g. ``"name"``).
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_shopping_lists(
            get_client(),
            page=page,
            per_page=per_page,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_create_shopping_list")
    def _create_shopping_list(name: str) -> dict[str, Any]:
        """Create a new shopping list for the household.

        Args:
            name: Display name for the list. Required.

        Returns:
            The newly created shopping list as a JSON-compatible dict.
        """
        return create_shopping_list(get_client(), name=name)

    @mcp.tool(name="mealie_get_shopping_list")
    def _get_shopping_list(list_id: str) -> dict[str, Any]:
        """Fetch a single shopping list by id, including its items.

        Args:
            list_id: UUID of the shopping list.

        Returns:
            The shopping list payload, with a ``listItems`` array, as a
            JSON-compatible dict.
        """
        return get_shopping_list(get_client(), list_id=list_id)

    @mcp.tool(name="mealie_update_shopping_list")
    def _update_shopping_list(list_id: str, name: str) -> dict[str, Any]:
        """Rename an existing shopping list.

        Only the name changes; the list's items and other fields are preserved.

        Args:
            list_id: UUID of the shopping list.
            name: New display name for the list.

        Returns:
            The updated shopping list payload as a JSON-compatible dict.
        """
        return update_shopping_list(get_client(), list_id=list_id, name=name)

    @mcp.tool(name="mealie_delete_shopping_list")
    def _delete_shopping_list(list_id: str) -> dict[str, Any]:
        """Delete a shopping list from Mealie by id.

        Args:
            list_id: UUID of the shopping list to delete.

        Returns:
            A canonical acknowledgement ``{"id": <list_id>, "deleted": True}``.
        """
        return delete_shopping_list(get_client(), list_id=list_id)

    @mcp.tool(name="mealie_add_recipe_to_shopping_list")
    def _add_recipe_to_shopping_list(
        list_id: str, recipe_id: str, scale: float = 1.0
    ) -> dict[str, Any]:
        """Add a recipe's ingredients to a shopping list.

        Args:
            list_id: UUID of the shopping list.
            recipe_id: UUID of the recipe whose ingredients to add.
            scale: Quantity multiplier. ``2.0`` adds a double batch. Defaults
                to ``1.0``.

        Returns:
            The updated shopping list payload, including ``listItems`` and
            ``recipeReferences``, as a JSON-compatible dict.
        """
        return add_recipe_to_shopping_list(
            get_client(), list_id=list_id, recipe_id=recipe_id, scale=scale
        )

    @mcp.tool(name="mealie_add_recipes_to_shopping_list")
    def _add_recipes_to_shopping_list(
        list_id: str, recipes: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Add several recipes' ingredients to a shopping list in one call.

        Args:
            list_id: UUID of the shopping list.
            recipes: Recipes to add. Each entry is an object with a required
                ``recipe_id`` and an optional ``scale`` (default ``1.0``), e.g.
                ``[{"recipe_id": "...", "scale": 2.0}, {"recipe_id": "..."}]``.

        Returns:
            The updated shopping list payload as a JSON-compatible dict.
        """
        return add_recipes_to_shopping_list(get_client(), list_id=list_id, recipes=recipes)

    @mcp.tool(name="mealie_remove_recipe_from_shopping_list")
    def _remove_recipe_from_shopping_list(
        list_id: str, recipe_id: str, scale: float = 1.0
    ) -> dict[str, Any]:
        """Remove a recipe's ingredients from a shopping list.

        Args:
            list_id: UUID of the shopping list.
            recipe_id: UUID of the recipe whose ingredients to remove.
            scale: Quantity multiplier to decrement by. Removing as much as was
                added drops the recipe reference entirely. Defaults to ``1.0``.

        Returns:
            The updated shopping list payload as a JSON-compatible dict.
        """
        return remove_recipe_from_shopping_list(
            get_client(), list_id=list_id, recipe_id=recipe_id, scale=scale
        )
