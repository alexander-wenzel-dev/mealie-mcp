"""Live test for the food lifecycle.

Stages a sentinel food, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
import json
from collections.abc import Iterator
from http import HTTPStatus

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.groups_multi_purpose_labels import (
    create_one_api_groups_labels_post,
    delete_one_api_groups_labels_item_id_delete,
)
from mealie_mcp.client.api.recipes_foods import update_one_api_foods_item_id_put
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_food import CreateIngredientFood
from mealie_mcp.client.models.create_ingredient_food_extras_type_0 import (
    CreateIngredientFoodExtrasType0,
)
from mealie_mcp.client.models.multi_purpose_label_create import MultiPurposeLabelCreate
from mealie_mcp.tools import recipes_foods
from mealie_mcp.tools._common import expect_dict

SEED_EXTRAS_KEY = "mcp_test_extras_key"


@pytest.fixture
def sentinel_label(mealie_client: AuthenticatedClient, sentinel_name: str) -> Iterator[str]:
    """Stage a multi purpose label to seed the food's `labelId`.

    No label tools exist yet, so the label goes through the generated client
    directly. The finalizer runs after the food fixture's, so the label
    outlives the food that references it.
    """
    response = create_one_api_groups_labels_post.sync_detailed(
        client=mealie_client,
        body=MultiPurposeLabelCreate(name=f"{sentinel_name}-label"),
    )
    assert response.status_code == HTTPStatus.OK, response.content
    label_id = str(json.loads(response.content)["id"])
    try:
        yield label_id
    finally:
        with contextlib.suppress(ToolError):
            expect_dict(
                "delete_label",
                delete_one_api_groups_labels_item_id_delete.sync_detailed(
                    label_id, client=mealie_client
                ),
            )


@pytest.fixture
def created_food(
    mealie_client: AuthenticatedClient, sentinel_name: str, sentinel_label: str
) -> Iterator[dict[str, str]]:
    """Stage a sentinel food via `create_food`, then seed two unexposed fields.

    Staging through the tool gives `create_food` live coverage for the
    descriptive fields. `extras` and `label_id` are body-model fields the
    food tools do not expose, so they are the ones a naive PUT would silently
    clobber. Both are seeded with a direct PUT built from the created payload,
    so an update that touches only exposed fields must leave them intact.
    """
    created = recipes_foods.create_food(
        mealie_client,
        name=sentinel_name,
        plural_name=f"{sentinel_name}-plural",
        description=f"{sentinel_name}-description",
        aliases=[f"{sentinel_name}-alias-1", f"{sentinel_name}-alias-2"],
    )
    item_id = str(created["id"])
    try:
        assert created["name"] == sentinel_name
        assert created["pluralName"] == f"{sentinel_name}-plural"
        assert created["description"] == f"{sentinel_name}-description"
        assert {alias["name"] for alias in created["aliases"]} == {
            f"{sentinel_name}-alias-1",
            f"{sentinel_name}-alias-2",
        }

        seed = CreateIngredientFood.from_dict(created)
        seed.additional_properties = {}
        extras_seed = CreateIngredientFoodExtrasType0()
        extras_seed[SEED_EXTRAS_KEY] = f"{sentinel_name}-extras"
        seed.extras = extras_seed
        seed.label_id = sentinel_label
        expect_dict(
            "seed_food_fields",
            update_one_api_foods_item_id_put.sync_detailed(
                item_id, client=mealie_client, body=seed
            ),
        )

        yield {"id": item_id, "name": sentinel_name, "label_id": sentinel_label}
    finally:
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=item_id)


@pytest.mark.live
def test_food_lifecycle(mealie_client: AuthenticatedClient, created_food: dict[str, str]) -> None:
    item_id = created_food["id"]
    name = created_food["name"]
    label_id = created_food["label_id"]

    seeded_aliases = {f"{name}-alias-1", f"{name}-alias-2"}

    fetched = recipes_foods.get_food(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == name
    assert fetched["pluralName"] == f"{name}-plural"
    assert fetched["description"] == f"{name}-description"
    assert {alias["name"] for alias in fetched["aliases"]} == seeded_aliases
    assert fetched["extras"][SEED_EXTRAS_KEY] == f"{name}-extras"
    assert fetched["labelId"] == label_id

    listing = recipes_foods.list_foods(mealie_client, search=name, per_page=100)
    assert any(f["id"] == item_id for f in listing["items"])

    renamed = f"{name}-renamed"
    updated = recipes_foods.update_food(mealie_client, item_id=item_id, name=renamed)
    assert updated["id"] == item_id
    assert updated["name"] == renamed
    assert updated["pluralName"] == f"{name}-plural"
    assert updated["description"] == f"{name}-description"
    assert {alias["name"] for alias in updated["aliases"]} == seeded_aliases
    assert updated["extras"][SEED_EXTRAS_KEY] == f"{name}-extras"
    assert updated["labelId"] == label_id

    updated = recipes_foods.update_food(
        mealie_client,
        item_id=item_id,
        plural_name=f"{name}-plural-2",
        description=f"{name}-description-2",
        aliases=[f"{name}-alias-3"],
    )
    assert updated["name"] == renamed
    assert updated["pluralName"] == f"{name}-plural-2"
    assert updated["description"] == f"{name}-description-2"
    assert {alias["name"] for alias in updated["aliases"]} == {f"{name}-alias-3"}
    assert updated["extras"][SEED_EXTRAS_KEY] == f"{name}-extras"
    assert updated["labelId"] == label_id

    refetched = recipes_foods.get_food(mealie_client, item_id=item_id)
    assert refetched["name"] == renamed
    assert refetched["pluralName"] == f"{name}-plural-2"
    assert refetched["description"] == f"{name}-description-2"
    assert {alias["name"] for alias in refetched["aliases"]} == {f"{name}-alias-3"}

    ack = recipes_foods.delete_food(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_food failed \(404"):
        recipes_foods.get_food(mealie_client, item_id=item_id)


@pytest.mark.live
def test_create_food_name_only_leaves_defaults(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    """A name-only create sends no optional fields, so Mealie's defaults apply."""
    created = recipes_foods.create_food(mealie_client, name=sentinel_name)
    item_id = str(created["id"])
    try:
        fetched = recipes_foods.get_food(mealie_client, item_id=item_id)
        assert fetched["pluralName"] is None
        assert fetched["description"] == ""
        assert fetched["aliases"] == []
    finally:
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=item_id)
