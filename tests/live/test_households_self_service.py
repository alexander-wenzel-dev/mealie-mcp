"""Live tests for the household's record of a recipe.

Stages a sentinel recipe, reads the household record before and after a
last-made update, and deletes the recipe even when the body fails so no
`mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
import datetime as dt
from collections.abc import Callable

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import households_self_service, recipe_crud


@pytest.mark.live
def test_household_recipe_reports_last_made_in_utc(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """A never-made recipe reads null; a set timestamp reads back in UTC by slug or id."""
    slug: str | None = None
    try:
        slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_id = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["id"]

        fresh = call_tool("mealie_get_household_recipe", {"slug_or_id": slug})
        assert fresh == {"recipeId": recipe_id, "lastMade": None}

        sent = dt.datetime(2026, 6, 1, 12, 0, tzinfo=dt.timezone(dt.timedelta(hours=2)))
        recipe_crud.update_last_made(mealie_client, slug_or_id=slug, timestamp=sent.isoformat())

        made = households_self_service.get_household_recipe(mealie_client, slug_or_id=recipe_id)
        assert made["recipeId"] == recipe_id
        returned = dt.datetime.fromisoformat(made["lastMade"])
        assert returned.utcoffset() == dt.timedelta(0)
        assert returned == sent
    finally:
        if slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
