"""Live tests for the household cookbook lifecycle.

Stages sentinel cookbooks and exercises the create, get, list, update, and
delete tools. The lifecycle test proves the stored ``queryFilterString`` both
round-trips and resolves real recipes, by tagging a sentinel recipe and asserting
it appears when the cookbook is passed to ``list_recipes``. The clobber test
proves the update tool's fetch-then-merge preserves ``public`` and ``position``,
two body-model fields the tool does not expose. Cleanup runs even when the body
fails so no `mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_cookbooks import (
    update_one_api_households_cookbooks_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_cook_book import CreateCookBook
from mealie_mcp.tools import households_cookbooks, organizer_tags, recipe_crud
from mealie_mcp.tools._common import expect_dict


@pytest.fixture
def created_cookbook(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel cookbook and tear it down."""
    created = households_cookbooks.create_cookbook(mealie_client, name=sentinel_name)
    item_id = created["id"]
    try:
        yield {"id": item_id}
    finally:
        with contextlib.suppress(ToolError):
            households_cookbooks.delete_cookbook(mealie_client, item_id=item_id)


@pytest.mark.live
def test_cookbook_lifecycle_filter_resolves_recipes(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    tag: dict[str, Any] | None = None
    recipe_slug: str | None = None
    cookbook_id: str | None = None
    try:
        tag = organizer_tags.create_tag(mealie_client, name=sentinel_name)
        recipe_slug = recipe_crud.create_recipe(mealie_client, name=sentinel_name)["slug"]
        recipe_crud.update_recipe(
            mealie_client,
            slug_or_id=recipe_slug,
            tags=[{"id": tag["id"], "name": tag["name"], "slug": tag["slug"]}],
        )

        query_filter_string = f'tags.id IN ["{tag["id"]}"]'
        created = households_cookbooks.create_cookbook(
            mealie_client,
            name=sentinel_name,
            description=f"{sentinel_name}-desc",
            query_filter_string=query_filter_string,
        )
        cookbook_id = created["id"]

        fetched = households_cookbooks.get_cookbook(mealie_client, item_id=cookbook_id)
        assert fetched["name"] == sentinel_name
        assert fetched["description"] == f"{sentinel_name}-desc"
        assert fetched["queryFilterString"] == query_filter_string

        listing = households_cookbooks.list_cookbooks(mealie_client, per_page=100)
        assert any(item["id"] == cookbook_id for item in listing["items"])

        # The stored filter is not just persisted text: passing the cookbook to
        # list_recipes must resolve to the tagged sentinel recipe. A filter that
        # parses but matches nothing would leave items empty and fail here.
        resolved = recipe_crud.list_recipes(mealie_client, cookbook=fetched["slug"], per_page=100)
        assert any(item["slug"] == recipe_slug for item in resolved["items"]), (
            f"recipe {recipe_slug} not resolved by cookbook filter {query_filter_string!r}"
        )

        # A name-only update must not clobber the stored filter: it survives the
        # PUT-replace and still resolves the recipe afterwards.
        renamed = households_cookbooks.update_cookbook(
            mealie_client, item_id=cookbook_id, name=f"{sentinel_name}-renamed"
        )
        assert renamed["name"] == f"{sentinel_name}-renamed"
        refetched = households_cookbooks.get_cookbook(mealie_client, item_id=cookbook_id)
        assert refetched["queryFilterString"] == query_filter_string
        resolved_after = recipe_crud.list_recipes(
            mealie_client, cookbook=refetched["slug"], per_page=100
        )
        assert any(item["slug"] == recipe_slug for item in resolved_after["items"]), (
            f"recipe {recipe_slug} no longer resolved after a name-only update"
        )

        ack = households_cookbooks.delete_cookbook(mealie_client, item_id=cookbook_id)
        assert ack == {"id": cookbook_id, "deleted": True}
        cookbook_id = None

        with pytest.raises(ToolError, match=r"Mealie get_cookbook failed \(404"):
            households_cookbooks.get_cookbook(mealie_client, item_id=created["id"])
    finally:
        if cookbook_id is not None:
            with contextlib.suppress(ToolError):
                households_cookbooks.delete_cookbook(mealie_client, item_id=cookbook_id)
        if recipe_slug is not None:
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=recipe_slug)
        if tag is not None:
            with contextlib.suppress(ToolError):
                organizer_tags.delete_tag(mealie_client, item_id=tag["id"])


def _force_public_and_position(client: AuthenticatedClient, item_id: str, *, position: int) -> None:
    """Set ``public=True`` and a fixed ``position`` on a cookbook via a direct PUT.

    Neither field is exposed by ``update_cookbook``. Seeding non-default values
    here lets the clobber test assert they survive a name-only update.
    """
    fetched = households_cookbooks.get_cookbook(client, item_id=item_id)
    body = CreateCookBook.from_dict(fetched)
    body.additional_properties = {}
    body.public = True
    body.position = position
    expect_dict(
        "seed_public_position",
        update_one_api_households_cookbooks_item_id_put.sync_detailed(
            item_id, client=client, body=body
        ),
    )


@pytest.mark.live
def test_update_preserves_public_and_position(
    mealie_client: AuthenticatedClient,
    created_cookbook: dict[str, str],
    sentinel_name: str,
) -> None:
    item_id = created_cookbook["id"]
    _force_public_and_position(mealie_client, item_id, position=99)

    staged = households_cookbooks.get_cookbook(mealie_client, item_id=item_id)
    assert staged["public"] is True
    assert staged["position"] == 99

    new_name = f"{sentinel_name}-renamed"
    updated = households_cookbooks.update_cookbook(mealie_client, item_id=item_id, name=new_name)
    assert updated["name"] == new_name

    after = households_cookbooks.get_cookbook(mealie_client, item_id=item_id)
    assert after["name"] == new_name
    # The name-only update must not reset the two unexposed fields to their
    # schema defaults (public=False, position=1); fetch-then-merge preserves them.
    assert after["public"] is True
    assert after["position"] == 99


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_create_cookbook_round_trips_through_wrapper(
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    description = f"{sentinel_name}-desc"
    created = call_tool(
        "mealie_create_cookbook", {"name": sentinel_name, "description": description}
    )
    assert isinstance(created, dict)
    item_id = created["id"]
    try:
        # name and description are both str; fetching both back catches a swap.
        fetched = call_tool("mealie_get_cookbook", {"item_id": item_id})
        assert isinstance(fetched, dict)
        assert fetched["name"] == sentinel_name
        assert fetched["description"] == description
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_cookbook", {"item_id": item_id})
