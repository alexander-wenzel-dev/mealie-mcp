"""Recipe bulk-action tools.

Mirrors `mealie_mcp.client.api.recipe_bulk_actions`. Exposes the synchronous
bulk endpoints under `/api/recipes/bulk-actions/`: tag, categorize, apply
settings, and delete many recipes in one call.

Recipes are addressed by slug throughout. Tag and categorize append the
supplied objects to each recipe's existing tags or categories rather than
replacing them, so both actions are additive. Apply-settings replaces the five
exposed settings on every targeted recipe; the endpoint cannot change lock
state. Each endpoint returns HTTP 200 with an empty body, so the tools return a
constructed acknowledgement.
"""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipe_bulk_actions import (
    bulk_categorize_recipes_api_recipes_bulk_actions_categorize_post,
    bulk_delete_recipes_api_recipes_bulk_actions_delete_post,
    bulk_settings_recipes_api_recipes_bulk_actions_settings_post,
    bulk_tag_recipes_api_recipes_bulk_actions_tag_post,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.assign_categories import AssignCategories
from mealie_mcp.client.models.assign_settings import AssignSettings
from mealie_mcp.client.models.assign_tags import AssignTags
from mealie_mcp.client.models.category_base import CategoryBase
from mealie_mcp.client.models.delete_recipes import DeleteRecipes
from mealie_mcp.client.models.recipe_settings import RecipeSettings
from mealie_mcp.client.models.tag_base import TagBase
from mealie_mcp.client.types import Response
from mealie_mcp.client_factory import ClientProvider
from mealie_mcp.tools._common import (
    ack_delete_bulk,
    raise_api_error,
    require_non_empty,
)


def _require_recipe_slugs(recipes: list[str]) -> None:
    """Raise a `ToolError` unless `recipes` holds at least one non-empty slug."""
    if not recipes:
        raise ToolError("recipes must contain at least one slug")
    for slug in recipes:
        require_non_empty("recipe slug", slug)


def _ack_bulk_action(
    action: str, response: Response[Any], recipes: list[str], effect: str
) -> dict[str, Any]:
    """Return a constructed acknowledgement after verifying a 200 response.

    The bulk tag, categorize, and settings endpoints all return HTTP 200 with an
    empty body, so there is no payload to decode. The acknowledgement echoes the
    recipes acted on under a flag named for the effect applied.
    """
    if response.status_code != HTTPStatus.OK:
        raise_api_error(action, int(response.status_code), response.content)
    return {"recipes": recipes, effect: True}


def tag_recipes(
    client: AuthenticatedClient, recipes: list[str], tags: list[dict[str, Any]]
) -> dict[str, Any]:
    """Add tags to each recipe. Returns a constructed acknowledgement.

    ``recipes`` are recipe slugs. Each entry of ``tags`` is a full tag object
    with ``name``, ``id``, and ``slug``. The endpoint appends the tags to each
    recipe's existing tags; it does not replace them.
    """
    _require_recipe_slugs(recipes)
    if not tags:
        raise ToolError("tags must contain at least one tag object")

    try:
        tag_models = [TagBase.from_dict(tag) for tag in tags]
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ToolError(f"tag_recipes tags invalid: {exc}") from exc

    response = bulk_tag_recipes_api_recipes_bulk_actions_tag_post.sync_detailed(
        client=client, body=AssignTags(recipes=recipes, tags=tag_models)
    )
    return _ack_bulk_action("tag_recipes", response, recipes, "tagged")


def categorize_recipes(
    client: AuthenticatedClient, recipes: list[str], categories: list[dict[str, Any]]
) -> dict[str, Any]:
    """Add categories to each recipe. Returns a constructed acknowledgement.

    ``recipes`` are recipe slugs. Each entry of ``categories`` is a full
    category object with ``name``, ``id``, and ``slug``. The endpoint appends the
    categories to each recipe's existing categories; it does not replace them.
    """
    _require_recipe_slugs(recipes)
    if not categories:
        raise ToolError("categories must contain at least one category object")

    try:
        category_models = [CategoryBase.from_dict(category) for category in categories]
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ToolError(f"categorize_recipes categories invalid: {exc}") from exc

    response = bulk_categorize_recipes_api_recipes_bulk_actions_categorize_post.sync_detailed(
        client=client, body=AssignCategories(recipes=recipes, categories=category_models)
    )
    return _ack_bulk_action("categorize_recipes", response, recipes, "categorized")


def apply_recipe_settings(
    client: AuthenticatedClient,
    recipes: list[str],
    public: bool,
    show_nutrition: bool,
    show_assets: bool,
    landscape_view: bool,
    disable_comments: bool,
) -> dict[str, Any]:
    """Overwrite five settings on each recipe. Returns a constructed acknowledgement.

    The endpoint replaces the settings object wholesale, so all five booleans
    are required and applied to every recipe. It cannot change lock state: it
    preserves each recipe's existing ``locked`` value.
    """
    _require_recipe_slugs(recipes)

    settings = RecipeSettings(
        public=public,
        show_nutrition=show_nutrition,
        show_assets=show_assets,
        landscape_view=landscape_view,
        disable_comments=disable_comments,
    )
    response = bulk_settings_recipes_api_recipes_bulk_actions_settings_post.sync_detailed(
        client=client, body=AssignSettings(recipes=recipes, settings=settings)
    )
    return _ack_bulk_action("apply_recipe_settings", response, recipes, "settings_applied")


def delete_recipes(client: AuthenticatedClient, recipes: list[str]) -> dict[str, Any]:
    """Delete each recipe by slug. Returns ``{"ids": recipes, "deleted": True}``."""
    _require_recipe_slugs(recipes)

    response = bulk_delete_recipes_api_recipes_bulk_actions_delete_post.sync_detailed(
        client=client, body=DeleteRecipes(recipes=recipes)
    )
    return ack_delete_bulk("delete_recipes", response, recipes)


def register(mcp: FastMCP, get_client: ClientProvider) -> None:
    """Register the recipe bulk-action tools on the given FastMCP instance."""

    @mcp.tool(name="mealie_tag_recipes")
    def _tag_recipes(recipes: list[str], tags: list[dict[str, Any]]) -> dict[str, Any]:
        """Add one or more tags to many recipes in a single call.

        This is additive: the tags are appended to each recipe's existing tags,
        not swapped in. To find the tag objects to pass, list tags first with
        ``mealie_list_tags``; each entry must be a full object, not a slug.

        The batch is not atomic. If any slug in ``recipes`` does not exist the
        whole call fails, but recipes processed before the bad one are already
        tagged, so retrying after the error can re-apply a tag.

        Args:
            recipes: Recipe slugs to tag. Must contain at least one slug.
            tags: Full tag objects, each with ``name``, ``id``, and ``slug`` (as
                returned by ``mealie_list_tags`` or ``mealie_get_tag``). A
                slug-only object does not resolve; the ``id`` is required.

        Returns:
            ``{"recipes": <slugs>, "tagged": True}``.
        """
        return tag_recipes(get_client(), recipes=recipes, tags=tags)

    @mcp.tool(name="mealie_categorize_recipes")
    def _categorize_recipes(recipes: list[str], categories: list[dict[str, Any]]) -> dict[str, Any]:
        """Add one or more categories to many recipes in a single call.

        This is additive: the categories are appended to each recipe's existing
        categories, not swapped in. To find the category objects to pass, list
        categories first with ``mealie_list_categories``; each entry must be a
        full object, not a slug.

        The batch is not atomic. If any slug in ``recipes`` does not exist the
        whole call fails, but recipes processed before the bad one are already
        categorized, so retrying after the error can re-apply a category.

        Args:
            recipes: Recipe slugs to categorize. Must contain at least one slug.
            categories: Full category objects, each with ``name``, ``id``, and
                ``slug`` (as returned by ``mealie_list_categories`` or
                ``mealie_get_category``). A slug-only object does not resolve;
                the ``id`` is required.

        Returns:
            ``{"recipes": <slugs>, "categorized": True}``.
        """
        return categorize_recipes(get_client(), recipes=recipes, categories=categories)

    @mcp.tool(name="mealie_apply_recipe_settings")
    def _apply_recipe_settings(
        recipes: list[str],
        public: bool,
        show_nutrition: bool,
        show_assets: bool,
        landscape_view: bool,
        disable_comments: bool,
    ) -> dict[str, Any]:
        """Overwrite display settings on many recipes in a single call.

        The endpoint replaces the whole settings object on every targeted
        recipe, so all five booleans are required with no defaults: any omitted
        field would reset to its default on every recipe. This tool cannot lock
        or unlock recipes; the endpoint preserves each recipe's existing lock
        state. Change lock state per recipe instead.

        The batch is not atomic. If any slug in ``recipes`` does not exist the
        whole call fails, but recipes processed before the bad one already carry
        the new settings.

        Args:
            recipes: Recipe slugs to update. Must contain at least one slug.
            public: Whether each recipe is publicly viewable.
            show_nutrition: Whether the nutrition panel is shown.
            show_assets: Whether the assets panel is shown.
            landscape_view: Whether the landscape layout is used.
            disable_comments: Whether comments are disabled.

        Returns:
            ``{"recipes": <slugs>, "settings_applied": True}``.
        """
        return apply_recipe_settings(
            get_client(),
            recipes=recipes,
            public=public,
            show_nutrition=show_nutrition,
            show_assets=show_assets,
            landscape_view=landscape_view,
            disable_comments=disable_comments,
        )

    @mcp.tool(name="mealie_delete_recipes")
    def _delete_recipes(recipes: list[str]) -> dict[str, Any]:
        """Delete many recipes by slug in a single call.

        High blast radius: every listed recipe is deleted. There is no undo.

        A nonexistent slug is silently skipped: Mealie still returns success and
        the acknowledgement echoes every slug requested, not a confirmation that
        each existed, so a mistyped slug goes unnoticed.

        Args:
            recipes: Recipe slugs to delete. Must contain at least one slug.

        Returns:
            A canonical batch acknowledgement
            ``{"ids": <slugs>, "deleted": True}``.
        """
        return delete_recipes(get_client(), recipes=recipes)
