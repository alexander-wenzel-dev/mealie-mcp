"""Live test for the food lifecycle.

Stages a sentinel food, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipes_foods import update_one_api_foods_item_id_put
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_food import CreateIngredientFood
from mealie_mcp.tools import recipes_foods

SEED_DESCRIPTION = "mcp-test-description"


@pytest.fixture
def created_food(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Stage a sentinel food via `create_food`, then seed a non-default field.

    Staging through the tool gives `create_food` live coverage. The non-default
    `description` is seeded with a direct PUT so the lifecycle test can verify
    that `update_food` preserves untouched fields when only `name` is changed.
    """
    created = recipes_foods.create_food(mealie_client, name=sentinel_name)
    item_id = created["id"]
    assert created["name"] == sentinel_name

    update_one_api_foods_item_id_put.sync_detailed(
        item_id,
        client=mealie_client,
        body=CreateIngredientFood(id=item_id, name=sentinel_name, description=SEED_DESCRIPTION),
    )
    try:
        yield {"id": item_id, "name": sentinel_name, "description": SEED_DESCRIPTION}
    finally:
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=item_id)


@pytest.mark.live
def test_food_lifecycle(mealie_client: AuthenticatedClient, created_food: dict[str, str]) -> None:
    item_id = created_food["id"]

    fetched = recipes_foods.get_food(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == created_food["name"]
    assert fetched["description"] == SEED_DESCRIPTION

    listing = recipes_foods.list_foods(mealie_client, search=created_food["name"], per_page=100)
    assert any(f["id"] == item_id for f in listing["items"])

    updated_name = f"{created_food['name']}-renamed"
    updated = recipes_foods.update_food(mealie_client, item_id=item_id, name=updated_name)
    assert updated["id"] == item_id
    assert updated["name"] == updated_name
    assert updated["description"] == SEED_DESCRIPTION

    ack = recipes_foods.delete_food(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_food failed \(404"):
        recipes_foods.get_food(mealie_client, item_id=item_id)
