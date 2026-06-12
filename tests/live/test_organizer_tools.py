"""Live test for the tool (equipment) lifecycle.

Stages a sentinel tool, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_self_service import (
    get_logged_in_user_household_api_households_self_get,
)
from mealie_mcp.client.api.organizer_tools import update_one_api_organizers_tools_item_id_put
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.recipe_tool_create import RecipeToolCreate
from mealie_mcp.tools import organizer_tools
from mealie_mcp.tools._common import expect_dict


@pytest.fixture
def created_tool(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, object]]:
    """Stage a sentinel tool via `create_tool`, then seed `households_with_tool`.

    Staging through the tool gives `create_tool` live coverage. `households_with_tool`
    is the only field on the create body model that `update_tool` does not expose,
    so it is the one a naive PUT would silently overwrite. It is seeded with a
    direct PUT carrying the current user's household id so the lifecycle test can
    verify that `update_tool` preserves the untouched field when only `name`
    is changed. Mealie's PUT silently drops household ids passed for this field
    and stores only the slug, so the seed uses the current user's household
    slug to round-trip cleanly through the GET-then-PUT merge.
    """
    self_household = expect_dict(
        "households_self",
        get_logged_in_user_household_api_households_self_get.sync_detailed(client=mealie_client),
    )
    households_seed = [str(self_household["slug"])]

    created = organizer_tools.create_tool(mealie_client, name=sentinel_name)
    item_id = created["id"]
    assert created["name"] == sentinel_name

    update_one_api_organizers_tools_item_id_put.sync_detailed(
        item_id,
        client=mealie_client,
        body=RecipeToolCreate(name=sentinel_name, households_with_tool=households_seed),
    )
    try:
        yield {
            "id": item_id,
            "name": sentinel_name,
            "households_with_tool": households_seed,
        }
    finally:
        with contextlib.suppress(ToolError):
            organizer_tools.delete_tool(mealie_client, item_id=item_id)


@pytest.mark.live
def test_tool_lifecycle(
    mealie_client: AuthenticatedClient, created_tool: dict[str, object]
) -> None:
    item_id = str(created_tool["id"])
    households_seed = created_tool["households_with_tool"]

    fetched = organizer_tools.get_tool(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == created_tool["name"]
    assert fetched["householdsWithTool"] == households_seed

    listing = organizer_tools.list_tools(
        mealie_client, search=str(created_tool["name"]), per_page=100
    )
    assert any(t["id"] == item_id for t in listing["items"])

    matched = next(t for t in listing["items"] if t["id"] == item_id)
    by_slug = organizer_tools.get_tool_by_slug(mealie_client, slug=matched["slug"])
    assert by_slug["id"] == item_id

    updated_name = f"{created_tool['name']}-renamed"
    updated = organizer_tools.update_tool(mealie_client, item_id=item_id, name=updated_name)
    assert updated["id"] == item_id
    assert updated["name"] == updated_name
    assert updated["householdsWithTool"] == households_seed

    ack = organizer_tools.delete_tool(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_tool failed \(404"):
        organizer_tools.get_tool(mealie_client, item_id=item_id)
