"""Live test for the unit lifecycle.

Stages a sentinel unit, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
import json
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipes_units import create_one_api_units_post
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_unit import CreateIngredientUnit
from mealie_mcp.tools import recipes_units

SEED_ABBREVIATION = "mcp-test-abbr"


@pytest.fixture
def created_unit(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel unit with a non-default abbreviation.

    Seeding a non-default body field lets the lifecycle test verify that
    `update_unit` preserves untouched fields when only `name` is changed.
    """
    response = create_one_api_units_post.sync_detailed(
        client=mealie_client,
        body=CreateIngredientUnit(name=sentinel_name, abbreviation=SEED_ABBREVIATION),
    )
    unit = json.loads(response.content)
    item_id = unit["id"]
    try:
        yield {"id": item_id, "name": sentinel_name, "abbreviation": SEED_ABBREVIATION}
    finally:
        with contextlib.suppress(ToolError):
            recipes_units.delete_unit(mealie_client, item_id=item_id)


@pytest.mark.live
def test_unit_lifecycle(mealie_client: AuthenticatedClient, created_unit: dict[str, str]) -> None:
    item_id = created_unit["id"]

    fetched = recipes_units.get_unit(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == created_unit["name"]
    assert fetched["abbreviation"] == SEED_ABBREVIATION

    listing = recipes_units.list_units(mealie_client, search=created_unit["name"], per_page=100)
    assert any(u["id"] == item_id for u in listing["items"])

    updated_name = f"{created_unit['name']}-renamed"
    updated = recipes_units.update_unit(mealie_client, item_id=item_id, name=updated_name)
    assert updated["id"] == item_id
    assert updated["name"] == updated_name
    assert updated["abbreviation"] == SEED_ABBREVIATION

    ack = recipes_units.delete_unit(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_unit failed \(404"):
        recipes_units.get_unit(mealie_client, item_id=item_id)
