"""Live test for the recipe comment lifecycle.

Stages a sentinel recipe, attaches a sentinel comment, exercises the read,
list, update, and delete tools, then tears both sentinels down. Cleanup runs
even when the test body fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
import time
from collections.abc import Callable, Iterator
from typing import Any

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

    ack = recipe_comments.delete_comment(mealie_client, comment_id=comment_id)
    assert ack == {"id": comment_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_comment failed \(404"):
        recipe_comments.get_comment(mealie_client, comment_id=comment_id)


def _relative_order(listing: dict[str, Any], *ids: str) -> list[str]:
    """The given ids in the order they appear in a comments listing.

    Keys on the known ids so comments outside this test do not affect the
    result. Asserts both ids are present before reporting their order.
    """
    items = listing["items"]
    assert isinstance(items, list)
    positions = {item["id"]: index for index, item in enumerate(items)}
    for comment_id in ids:
        assert comment_id in positions, f"comment {comment_id} not found in listing"
    return sorted(ids, key=lambda comment_id: positions[comment_id])


@pytest.mark.live
def test_list_comments_order_direction_flips_relative_order(
    mealie_client: AuthenticatedClient,
    created_recipe: dict[str, str],
    sentinel_name: str,
) -> None:
    """``order_direction`` reverses the relative order of two comments.

    Two sentinel comments are created in sequence with a one second gap so
    their server-assigned ``createdAt`` differ. Listing ascending then
    descending by ``createdAt`` must flip their relative order. The assertion
    keys on the two known ids so unrelated comments do not affect it.
    """
    recipe_id = created_recipe["id"]
    first = recipe_comments.create_comment(
        mealie_client, recipe_id=recipe_id, text=f"{sentinel_name}-order-a"
    )
    time.sleep(1.0)
    second = recipe_comments.create_comment(
        mealie_client, recipe_id=recipe_id, text=f"{sentinel_name}-order-b"
    )
    try:
        ascending = _relative_order(
            recipe_comments.list_comments(
                mealie_client, per_page=100, order_by="createdAt", order_direction="asc"
            ),
            first["id"],
            second["id"],
        )
        descending = _relative_order(
            recipe_comments.list_comments(
                mealie_client, per_page=100, order_by="createdAt", order_direction="desc"
            ),
            first["id"],
            second["id"],
        )
        assert ascending == [first["id"], second["id"]]
        assert descending == [second["id"], first["id"]]
    finally:
        for comment_id in (first["id"], second["id"]):
            with contextlib.suppress(ToolError):
                recipe_comments.delete_comment(mealie_client, comment_id=comment_id)


@pytest.mark.live
def test_create_comment_round_trips_through_wrapper(
    created_recipe: dict[str, str],
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    text = f"{sentinel_name}-comment"
    created = call_tool("mealie_create_comment", {"recipe_id": created_recipe["id"], "text": text})
    assert isinstance(created, dict)
    comment_id = created["id"]
    try:
        # recipe_id and text are both str; asserting the text lands as text catches a swap.
        assert created["text"] == text
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_comment", {"comment_id": comment_id})
