"""Recipe CRUD tools.

Mirrors `mealie_mcp.client.api.recipe_crud`. Exposes the recipe lifecycle
operations: list, create, read, duplicate, scrape from URL or raw payload,
patch the last-made timestamp, and delete.
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
    update_last_made_api_recipes_slug_last_made_patch,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_recipe import CreateRecipe
from mealie_mcp.client.models.recipe_duplicate import RecipeDuplicate
from mealie_mcp.client.models.recipe_last_made import RecipeLastMade
from mealie_mcp.client.models.scrape_recipe import ScrapeRecipe
from mealie_mcp.client.models.scrape_recipe_data import ScrapeRecipeData
from mealie_mcp.client.types import UNSET
from mealie_mcp.client_factory import build_client
from mealie_mcp.tools._common import (
    expect_dict,
    expect_str,
    parse_order_direction,
    raise_api_error,
    require_non_empty,
    require_per_page,
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
    if response.status_code != HTTPStatus.OK:
        raise_api_error("delete_recipe", int(response.status_code), response.content)
    return {"id": slug_or_id, "deleted": True}


def list_recipes(
    client: AuthenticatedClient,
    page: int = 1,
    per_page: int = 50,
    search: str | None = None,
    categories: list[str] | None = None,
    tags: list[str] | None = None,
    order_by: str | None = None,
    order_direction: Literal["asc", "desc"] | None = None,
) -> dict[str, Any]:
    """List recipes, paginated. Returns the pagination envelope."""
    require_per_page(per_page)
    response = get_all_api_recipes_get.sync_detailed(
        client=client,
        page=page,
        per_page=per_page,
        search=search if search is not None else UNSET,
        categories=categories if categories is not None else UNSET,
        tags=tags if tags is not None else UNSET,
        order_by=order_by if order_by is not None else UNSET,
        order_direction=parse_order_direction(order_direction),
    )
    return expect_dict("list_recipes", response)


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
            url=url if url is not None else UNSET,
        ),
    )
    slug = expect_str("create_recipe_from_html_or_json", response, HTTPStatus.CREATED)
    return {"slug": slug}


def register(mcp: FastMCP) -> None:
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
        return create_recipe(build_client(), name=name)

    @mcp.tool(name="mealie_get_recipe")
    def _get_recipe(slug_or_id: str) -> dict[str, Any]:
        """Fetch a single recipe from Mealie by slug or id.

        Args:
            slug_or_id: A recipe slug (e.g. ``"my-recipe"``) or UUID.

        Returns:
            The full Mealie recipe payload as a JSON-compatible dict.
        """
        return get_recipe(build_client(), slug_or_id=slug_or_id)

    @mcp.tool(name="mealie_delete_recipe")
    def _delete_recipe(slug_or_id: str) -> dict[str, Any]:
        """Delete a recipe from Mealie by slug or id.

        Args:
            slug_or_id: A recipe slug or UUID.

        Returns:
            A canonical acknowledgement ``{"id": <slug_or_id>, "deleted": True}``.
        """
        return delete_recipe(build_client(), slug_or_id=slug_or_id)

    @mcp.tool(name="mealie_list_recipes")
    def _list_recipes(
        page: int = 1,
        per_page: int = 50,
        search: str | None = None,
        categories: list[str] | None = None,
        tags: list[str] | None = None,
        order_by: str | None = None,
        order_direction: Literal["asc", "desc"] | None = None,
    ) -> dict[str, Any]:
        """List recipes from Mealie, paginated and optionally filtered.

        Args:
            page: 1-indexed page number. Defaults to 1.
            per_page: Page size. Defaults to 50. Capped at 100.
            search: Optional free-text search.
            categories: Optional list of category slugs to filter by.
            tags: Optional list of tag slugs to filter by.
            order_by: Optional column name to sort on.
            order_direction: ``"asc"`` or ``"desc"``.

        Returns:
            A pagination envelope with ``items`` and pagination metadata.
        """
        return list_recipes(
            build_client(),
            page=page,
            per_page=per_page,
            search=search,
            categories=categories,
            tags=tags,
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
        return duplicate_recipe(build_client(), slug_or_id=slug_or_id, name=name)

    @mcp.tool(name="mealie_update_last_made")
    def _update_last_made(slug_or_id: str, timestamp: str) -> dict[str, Any]:
        """Set a recipe's last-made timestamp.

        Args:
            slug_or_id: Recipe slug or UUID.
            timestamp: ISO 8601 datetime string (e.g. ``"2026-06-01T12:00:00Z"``).

        Returns:
            The updated recipe payload as a JSON-compatible dict.
        """
        return update_last_made(build_client(), slug_or_id=slug_or_id, timestamp=timestamp)

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
            build_client(),
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
            build_client(),
            data=data,
            include_tags=include_tags,
            include_categories=include_categories,
            url=url,
        )
