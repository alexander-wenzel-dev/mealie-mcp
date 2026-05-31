"""Live test for the recipe CRUD lifecycle.

Creates a sentinel recipe, reads it back, deletes it, and asserts that a
follow-up read raises a `ToolError`. The fixture finalizer also attempts to
delete the recipe so leftover state never lingers after a failed test body.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_crud


@pytest.fixture
def created_recipe(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel recipe and ensure it is removed on teardown."""
    created = recipe_crud.create_recipe(mealie_client, name=sentinel_name)
    try:
        yield {"slug": created["slug"], "name": sentinel_name}
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=created["slug"])


@pytest.mark.live
def test_recipe_crud_lifecycle(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> None:
    slug = created_recipe["slug"]

    fetched = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
    assert fetched["slug"] == slug
    assert fetched["name"] == created_recipe["name"]

    recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)

    with pytest.raises(ToolError, match=r"get_recipe failed \(404"):
        recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
