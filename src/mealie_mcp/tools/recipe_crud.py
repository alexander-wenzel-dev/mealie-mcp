"""Recipe CRUD tools.

Mirrors `mealie_mcp.client.api.recipe_crud`. Exposes the recipe lifecycle
operations: list, create, read, duplicate, scrape from URL or raw payload,
patch the last-made timestamp, edit fields, and delete.
"""

from __future__ import annotations

import datetime as dt
from http import HTTPStatus
from typing import Any, Literal

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipe_crud import (
    create_one_api_recipes_post,
    create_recipe_from_html_or_json_api_recipes_create_html_or_json_post,
    delete_one_api_recipes_slug_delete,
    duplicate_one_api_recipes_slug_duplicate_post,
    get_all_api_recipes_get,
    get_one_api_recipes_slug_get,
    parse_recipe_url_api_recipes_create_url_post,
    patch_one_api_recipes_slug_patch,
    suggest_recipes_api_recipes_suggestions_get,
    update_last_made_api_recipes_slug_last_made_patch,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_recipe import CreateRecipe
from mealie_mcp.client.models.recipe import Recipe
from mealie_mcp.client.models.recipe_duplicate import RecipeDuplicate
from mealie_mcp.client.models.recipe_last_made import RecipeLastMade
from mealie_mcp.client.models.scrape_recipe import ScrapeRecipe
from mealie_mcp.client.models.scrape_recipe_data import ScrapeRecipeData
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete,
    expect_dict,
    expect_str,
    parse_order_direction,
    require_non_empty,
    require_per_page,
    to_unset,
)


def create_recipe(client: AuthenticatedClient, name: str) -> dict[str, str]:
    """Create a recipe with the given name. Returns ``{"slug": ...}``."""
    require_non_empty("name", name)

    response = create_one_api_recipes_post.sync_detailed(
        client=client, body=CreateRecipe(name=name)
    )
    slug = expect_str("create_recipe", response, HTTPStatus.CREATED)
    return {"slug": slug}


def get_recipe(client: AuthenticatedClient, slug_or_id: str) -> dict[str, Any]:
    """Fetch a recipe by slug or id. Returns the full recipe payload."""
    require_non_empty("slug_or_id", slug_or_id)

    response = get_one_api_recipes_slug_get.sync_detailed(slug_or_id, client=client)
    return expect_dict("get_recipe", response)


def delete_recipe(client: AuthenticatedClient, slug_or_id: str) -> dict[str, Any]:
    """Delete a recipe by slug or id. Returns ``{"id": slug_or_id, "deleted": True}``."""
    require_non_empty("slug_or_id", slug_or_id)

    response = delete_one_api_recipes_slug_delete.sync_detailed(slug_or_id, client=client)
    return ack_delete("delete_recipe", response, slug_or_id)


def list_recipes(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    categories: list[str] | None = None,
    tags: list[str] | None = None,
    tools: list[str] | None = None,
    foods: list[str] | None = None,
    households: list[str] | None = None,
    cookbook: str | None = None,
    require_all_categories: bool = False,
    require_all_tags: bool = False,
    require_all_tools: bool = False,
    require_all_foods: bool = False,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List recipes, paginated. Returns the pagination envelope."""
    require_per_page(per_page)
    response = get_all_api_recipes_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=to_unset(search),
        categories=to_unset(categories),
        tags=to_unset(tags),
        tools=to_unset(tools),
        foods=to_unset(foods),
        households=to_unset(households),
        cookbook=to_unset(cookbook),
        require_all_categories=require_all_categories,
        require_all_tags=require_all_tags,
        require_all_tools=require_all_tools,
        require_all_foods=require_all_foods,
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_recipes", response)


def suggest_recipes(
    client: AuthenticatedClient,
    foods: list[str] | None = None,
    tools: list[str] | None = None,
    limit: int = 10,
    max_missing_foods: int = 5,
    max_missing_tools: int = 5,
    include_foods_on_hand: bool = True,
    include_tools_on_hand: bool = True,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """Suggest recipes matching the supplied foods and tools. Returns the items envelope."""
    response = suggest_recipes_api_recipes_suggestions_get.sync_detailed(
        client=client,
        foods=to_unset(foods),
        tools=to_unset(tools),
        limit=limit,
        max_missing_foods=max_missing_foods,
        max_missing_tools=max_missing_tools,
        include_foods_on_hand=include_foods_on_hand,
        include_tools_on_hand=include_tools_on_hand,
        order_by=to_unset(order_by),
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("suggest_recipes", response)


def duplicate_recipe(
    client: AuthenticatedClient, slug_or_id: str, name: str | None = None
) -> dict[str, Any]:
    """Duplicate an existing recipe. Returns the new recipe payload."""
    require_non_empty("slug_or_id", slug_or_id)

    body = RecipeDuplicate(name=name) if name is not None else RecipeDuplicate()
    response = duplicate_one_api_recipes_slug_duplicate_post.sync_detailed(
        slug_or_id, client=client, body=body
    )
    return expect_dict("duplicate_recipe", response, HTTPStatus.CREATED)


def update_last_made(
    client: AuthenticatedClient, slug_or_id: str, timestamp: str
) -> dict[str, Any]:
    """Patch a recipe's last-made timestamp. Returns the updated recipe payload."""
    require_non_empty("slug_or_id", slug_or_id)
    require_non_empty("timestamp", timestamp)

    try:
        parsed_timestamp = dt.datetime.fromisoformat(timestamp)
    except ValueError as exc:
        raise ToolError(f"timestamp must be an ISO 8601 datetime: {exc}") from exc

    response = update_last_made_api_recipes_slug_last_made_patch.sync_detailed(
        slug_or_id, client=client, body=RecipeLastMade(timestamp=parsed_timestamp)
    )
    return expect_dict("update_last_made", response)


_UPDATE_RECIPE_FIELD_MAP: dict[str, str] = {
    "name": "name",
    "description": "description",
    "recipe_yield": "recipeYield",
    "total_time": "totalTime",
    "prep_time": "prepTime",
    "perform_time": "performTime",
    "recipe_ingredient": "recipeIngredient",
    "recipe_instructions": "recipeInstructions",
    "notes": "notes",
    "tags": "tags",
    "recipe_category": "recipeCategory",
}


def update_recipe(
    client: AuthenticatedClient,
    slug_or_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    recipe_yield: str | None = None,
    total_time: str | None = None,
    prep_time: str | None = None,
    perform_time: str | None = None,
    recipe_ingredient: list[dict[str, Any]] | None = None,
    recipe_instructions: list[dict[str, Any]] | None = None,
    notes: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    recipe_category: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Patch selected fields on a recipe. Returns the updated recipe payload."""
    require_non_empty("slug_or_id", slug_or_id)

    supplied: dict[str, Any] = {
        "name": name,
        "description": description,
        "recipe_yield": recipe_yield,
        "total_time": total_time,
        "prep_time": prep_time,
        "perform_time": perform_time,
        "recipe_ingredient": recipe_ingredient,
        "recipe_instructions": recipe_instructions,
        "notes": notes,
        "tags": tags,
        "recipe_category": recipe_category,
    }
    patch: dict[str, Any] = {
        _UPDATE_RECIPE_FIELD_MAP[key]: value for key, value in supplied.items() if value is not None
    }
    if not patch:
        raise ToolError("update_recipe requires at least one field to update")

    try:
        body = Recipe.from_dict(patch)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ToolError(f"update_recipe payload invalid: {exc}") from exc

    response = patch_one_api_recipes_slug_patch.sync_detailed(slug_or_id, client=client, body=body)
    return expect_dict("update_recipe", response)


def parse_recipe_url(
    client: AuthenticatedClient,
    url: str,
    include_tags: bool = False,
    include_categories: bool = False,
) -> dict[str, str]:
    """Scrape a recipe from a URL and persist it. Returns ``{"slug": ...}``."""
    require_non_empty("url", url)

    response = parse_recipe_url_api_recipes_create_url_post.sync_detailed(
        client=client,
        body=ScrapeRecipe(
            url=url, include_tags=include_tags, include_categories=include_categories
        ),
    )
    slug = expect_str("parse_recipe_url", response, HTTPStatus.CREATED)
    return {"slug": slug}


def create_recipe_from_html_or_json(
    client: AuthenticatedClient,
    data: str,
    include_tags: bool = False,
    include_categories: bool = False,
    url: str | None = None,
) -> dict[str, str]:
    """Persist a recipe from raw HTML or a JSON-LD string. Returns ``{"slug": ...}``."""
    require_non_empty("data", data)

    response = create_recipe_from_html_or_json_api_recipes_create_html_or_json_post.sync_detailed(
        client=client,
        body=ScrapeRecipeData(
            data=data,
            include_tags=include_tags,
            include_categories=include_categories,
            url=to_unset(url),
        ),
    )
    slug = expect_str("create_recipe_from_html_or_json", response, HTTPStatus.CREATED)
    return {"slug": slug}


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the recipe CRUD tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_create_recipe")
    def _create_recipe(name: str) -> dict[str, str]:
        """Create a recipe in Mealie.

        Args:
            name: Human readable recipe name. Required, must be non-empty.

        Returns:
            ``{"slug": <slug>}`` where ``slug`` is the URL-safe identifier
            Mealie assigned to the new recipe.
        """
        return create_recipe(get_client(), name=name)

    @mcp.tool(name="mealie_get_recipe")
    def _get_recipe(slug_or_id: str) -> dict[str, Any]:
        """Fetch a single recipe from Mealie by slug or id.

        Args:
            slug_or_id: A recipe slug (e.g. ``"my-recipe"``) or UUID.

        Returns:
            The full Mealie recipe payload as a JSON-compatible dict.
        """
        return get_recipe(get_client(), slug_or_id=slug_or_id)

    @mcp.tool(name="mealie_delete_recipe")
    def _delete_recipe(slug_or_id: str) -> dict[str, Any]:
        """Delete a recipe from Mealie by slug or id.

        Args:
            slug_or_id: A recipe slug or UUID.

        Returns:
            A canonical acknowledgement ``{"id": <slug_or_id>, "deleted": True}``.
        """
        return delete_recipe(get_client(), slug_or_id=slug_or_id)

    @mcp.tool(name="mealie_list_recipes")
    def _list_recipes(
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        tools: list[str] | None = None,
        foods: list[str] | None = None,
        households: list[str] | None = None,
        cookbook: str | None = None,
        require_all_categories: bool = False,
        require_all_tags: bool = False,
        require_all_tools: bool = False,
        require_all_foods: bool = False,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List recipes from Mealie, paginated and optionally filtered.

        By default a recipe matches when it carries any one of the supplied
        ``categories``/``tags``/``tools``/``foods`` values; set the matching
        ``require_all_*`` flag to require every supplied value instead.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50. Capped at 100.
            search: Optional free-text search.
            categories: Optional list of category slugs to filter by.
            tags: Optional list of tag slugs to filter by.
            tools: Optional list of tool (equipment) slugs to filter by.
            foods: Optional list of food ids to filter by. Foods have no slug,
                so this filter takes the food id (a UUID).
            households: Optional list of household slugs to filter by.
            cookbook: Optional cookbook slug or id. Restricts results to the
                recipes that cookbook's saved filter selects.
            require_all_categories: Require every value in ``categories`` rather
                than any. Defaults to False.
            require_all_tags: Require every value in ``tags`` rather than any.
                Defaults to False.
            require_all_tools: Require every value in ``tools`` rather than any.
                Defaults to False.
            require_all_foods: Require every value in ``foods`` rather than any.
                Defaults to False.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_recipes(
            get_client(),
            page=page,
            per_page=per_page,
            search=search,
            categories=categories,
            tags=tags,
            tools=tools,
            foods=foods,
            households=households,
            cookbook=cookbook,
            require_all_categories=require_all_categories,
            require_all_tags=require_all_tags,
            require_all_tools=require_all_tools,
            require_all_foods=require_all_foods,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_suggest_recipes")
    def _suggest_recipes(
        foods: list[str] | None = None,
        tools: list[str] | None = None,
        limit: int = 10,
        max_missing_foods: int = 5,
        max_missing_tools: int = 5,
        include_foods_on_hand: bool = True,
        include_tools_on_hand: bool = True,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """Suggest recipes you can make from a set of foods on hand.

        Mealie ranks recipes by how well their ingredients match the supplied
        ``foods`` (and optionally ``tools``), tolerating a bounded number of
        missing items. Use this for "what can I make from what I have" rather
        than browsing the full recipe list.

        Args:
            foods: Optional list of food ids (UUIDs) on hand. Foods have no
                slug, so this takes the food id.
            tools: Optional list of tool (equipment) ids (UUIDs) on hand.
            limit: Maximum number of suggestions to return. Defaults to 10.
            max_missing_foods: Largest number of unmatched foods a recipe may
                require and still be suggested. Defaults to 5.
            max_missing_tools: Largest number of unmatched tools a recipe may
                require and still be suggested. Defaults to 5.
            include_foods_on_hand: Include the supplied foods when scoring.
                Defaults to True.
            include_tools_on_hand: Include the supplied tools when scoring.
                Defaults to True.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A dict with ``items``, each carrying the matched ``recipe`` summary
            plus its ``missingFoods`` and ``missingTools``.
        """
        return suggest_recipes(
            get_client(),
            foods=foods,
            tools=tools,
            limit=limit,
            max_missing_foods=max_missing_foods,
            max_missing_tools=max_missing_tools,
            include_foods_on_hand=include_foods_on_hand,
            include_tools_on_hand=include_tools_on_hand,
            order_by=order_by,
            order_direction=order_direction,
        )

    @mcp.tool(name="mealie_duplicate_recipe")
    def _duplicate_recipe(slug_or_id: str, name: str | None = None) -> dict[str, Any]:
        """Duplicate an existing recipe under an optional new name.

        Args:
            slug_or_id: Recipe slug or UUID to duplicate.
            name: Optional name for the new copy. If omitted, Mealie appends a
                suffix to the original name.

        Returns:
            The newly created recipe payload as a JSON-compatible dict.
        """
        return duplicate_recipe(get_client(), slug_or_id=slug_or_id, name=name)

    @mcp.tool(name="mealie_update_recipe")
    def _update_recipe(
        slug_or_id: str,
        name: str | None = None,
        description: str | None = None,
        recipe_yield: str | None = None,
        total_time: str | None = None,
        prep_time: str | None = None,
        perform_time: str | None = None,
        recipe_ingredient: list[dict[str, Any]] | None = None,
        recipe_instructions: list[dict[str, Any]] | None = None,
        notes: list[dict[str, Any]] | None = None,
        tags: list[dict[str, Any]] | None = None,
        recipe_category: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Edit fields on an existing Mealie recipe.

        Only the fields supplied are sent; omitted fields are left unchanged.
        At least one field beyond ``slug_or_id`` must be provided. List fields
        replace the existing value wholesale; there is no per-item merge.

        Args:
            slug_or_id: Recipe slug or UUID.
            name: New human-readable recipe name. Changing the name causes
                Mealie to reslug the recipe; subsequent calls must use the
                returned slug.
            description: New free-text description.
            recipe_yield: Human-readable yield (e.g. ``"4 servings"``).
            total_time: Human-readable total time (e.g. ``"45 minutes"``).
            prep_time: Human-readable preparation time.
            perform_time: Human-readable active cooking time.
            recipe_ingredient: Full ingredient list as Mealie ingredient dicts.
                Each item accepts keys like ``note``, ``quantity``, ``unit``,
                ``food``, ``title``, ``display``, ``originalText``.
            recipe_instructions: Full step list. Each item must have ``text``
                and may include ``title`` and ``summary``.
            notes: Full notes list. Each item must have ``title`` and ``text``.
            tags: Full tag list. Each item must have ``name`` and ``slug`` of
                an existing tag.
            recipe_category: Full category list. Each item must have ``name``
                and ``slug`` of an existing category.

        Returns:
            The updated recipe payload as a JSON-compatible dict.
        """
        return update_recipe(
            get_client(),
            slug_or_id=slug_or_id,
            name=name,
            description=description,
            recipe_yield=recipe_yield,
            total_time=total_time,
            prep_time=prep_time,
            perform_time=perform_time,
            recipe_ingredient=recipe_ingredient,
            recipe_instructions=recipe_instructions,
            notes=notes,
            tags=tags,
            recipe_category=recipe_category,
        )

    @mcp.tool(name="mealie_update_last_made")
    def _update_last_made(slug_or_id: str, timestamp: str) -> dict[str, Any]:
        """Set a recipe's last-made timestamp.

        Args:
            slug_or_id: Recipe slug or UUID.
            timestamp: ISO 8601 datetime string (e.g. ``"2026-06-01T12:00:00Z"``).

        Returns:
            The updated recipe payload as a JSON-compatible dict.
        """
        return update_last_made(get_client(), slug_or_id=slug_or_id, timestamp=timestamp)

    @mcp.tool(name="mealie_parse_recipe_url")
    def _parse_recipe_url(
        url: str, include_tags: bool = False, include_categories: bool = False
    ) -> dict[str, str]:
        """Scrape a recipe from a URL and persist it in Mealie.

        Args:
            url: URL of a recipe page Mealie can scrape.
            include_tags: Persist tags found in the scrape. Defaults to False.
            include_categories: Persist categories found in the scrape.
                Defaults to False.

        Returns:
            ``{"slug": <slug>}`` for the newly created recipe.
        """
        return parse_recipe_url(
            get_client(),
            url=url,
            include_tags=include_tags,
            include_categories=include_categories,
        )

    @mcp.tool(name="mealie_create_recipe_from_html_or_json")
    def _create_recipe_from_html_or_json(
        data: str,
        include_tags: bool = False,
        include_categories: bool = False,
        url: str | None = None,
    ) -> dict[str, str]:
        """Persist a recipe from raw HTML or a JSON-LD string.

        Args:
            data: HTML page source or a schema.org/Recipe JSON-LD string.
            include_tags: Persist tags found in the parsed content. Defaults to
                False.
            include_categories: Persist categories found in the parsed content.
                Defaults to False.
            url: Optional source URL to record alongside the recipe.

        Returns:
            ``{"slug": <slug>}`` for the newly created recipe.
        """
        return create_recipe_from_html_or_json(
            get_client(),
            data=data,
            include_tags=include_tags,
            include_categories=include_categories,
            url=url,
        )
