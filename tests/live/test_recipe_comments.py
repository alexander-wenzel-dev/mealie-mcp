"""Live test for the recipe comment lifecycle.

Stages a sentinel recipe, attaches a sentinel comment, exercises the read,
list, update, and delete tools, then tears both sentinels down. Cleanup runs
even when the test body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_comments, recipe_crud


@pytest.fixture
def created_recipe(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a parent recipe so comments have something to attach to."""
    created = recipe_crud.create_recipe(mealie_client, name=sentinel_name)
    slug = created["slug"]
    try:
        recipe = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)
        yield {"slug": slug, "id": recipe["id"]}
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.fixture
def created_comment(
    mealie_client: AuthenticatedClient, created_recipe: dict[str, str]
) -> Iterator[dict[str, str]]:
    """Attach a sentinel comment to the parent recipe and tear it down."""
    initial_text = "mcp-test-comment"
    created = recipe_comments.create_comment(
        mealie_client, recipe_id=created_recipe["id"], text=initial_text
    )
    comment_id = created["id"]
    try:
        yield {"id": comment_id, "text": initial_text}
    finally:
        with contextlib.suppress(ToolError):
            recipe_comments.delete_comment(mealie_client, comment_id=comment_id)


@pytest.mark.live
def test_recipe_comment_lifecycle(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    created_comment: dict[str, str],
) -> None:
    comment_id = created_comment["id"]
    slug = created_recipe["slug"]

    fetched = recipe_comments.get_comment(mealie_client, comment_id=comment_id)
    assert fetched["id"] == comment_id
    assert fetched["text"] == created_comment["text"]

    recipe_scoped = recipe_comments.list_recipe_comments(mealie_client, slug=slug)
    assert any(c["id"] == comment_id for c in recipe_scoped)

    listing = recipe_comments.list_comments(mealie_client, page=1, per_page=100)
    assert any(c["id"] == comment_id for c in listing["items"])

    updated_text = "mcp-test-comment-updated"
    updated = recipe_comments.update_comment(
        mealie_client, comment_id=comment_id, text=updated_text
    )
    assert updated["id"] == comment_id
    assert updated["text"] == updated_text

    recipe_comments.delete_comment(mealie_client, comment_id=comment_id)

    with pytest.raises(ToolError, match=r"get_comment failed \(404"):
        recipe_comments.get_comment(mealie_client, comment_id=comment_id)
