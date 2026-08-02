"""Live test for the food lifecycle.

Stages a sentinel food, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable, Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_self_service import (
    get_logged_in_user_household_api_households_self_get,
)
from mealie_mcp.client.api.recipes_foods import update_one_api_foods_item_id_put
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_food import CreateIngredientFood
from mealie_mcp.client.models.create_ingredient_food_extras_type_0 import (
    CreateIngredientFoodExtrasType0,
)
from mealie_mcp.tools import groups_multi_purpose_labels, recipes_foods
from mealie_mcp.tools._common import expect_dict

SEED_EXTRAS_KEY = "mcp_test_extras_key"


@pytest.fixture
def household_slug(mealie_client: AuthenticatedClient) -> str:
    """Slug of the token's own household, the value `householdsWithIngredientFood` takes.

    Mealie matches that list by slug and silently drops entries it cannot
    resolve, and the slug differs per instance. Scoping the food to the token's
    own household keeps it visible to the tests that read it back.
    """
    household = expect_dict(
        "get_own_household",
        get_logged_in_user_household_api_households_self_get.sync_detailed(client=mealie_client),
    )
    return str(household["slug"])


@pytest.fixture
def sentinel_label(mealie_client: AuthenticatedClient, sentinel_name: str) -> Iterator[str]:
    """Stage a multi purpose label for the food's `label_id`.

    The finalizer runs after the food fixture's, so the label outlives the food
    that references it.
    """
    label = groups_multi_purpose_labels.create_label(mealie_client, name=f"{sentinel_name}-label")
    label_id = str(label["id"])
    try:
        yield label_id
    finally:
        with contextlib.suppress(ToolError):
            groups_multi_purpose_labels.delete_label(mealie_client, item_id=label_id)


@pytest.fixture
def created_food(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
    sentinel_label: str,
    household_slug: str,
) -> Iterator[dict[str, str]]:
    """Stage a sentinel food via `create_food`, then seed two unexposed fields.

    Staging through the tool gives `create_food` live coverage for the
    descriptive fields and for `label_id`. `extras` and
    `households_with_ingredient_food` are body-model fields the food tools do
    not expose, so they are the ones a naive PUT would silently clobber. Both
    are seeded with a direct PUT built from the created payload, so an update
    that touches only exposed fields must leave them intact.
    """
    created = recipes_foods.create_food(
        mealie_client,
        name=sentinel_name,
        plural_name=f"{sentinel_name}-plural",
        description=f"{sentinel_name}-description",
        aliases=[f"{sentinel_name}-alias-1", f"{sentinel_name}-alias-2"],
        label_id=sentinel_label,
    )
    item_id = str(created["id"])
    try:
        assert created["name"] == sentinel_name
        assert created["pluralName"] == f"{sentinel_name}-plural"
        assert created["description"] == f"{sentinel_name}-description"
        assert created["labelId"] == sentinel_label
        assert {alias["name"] for alias in created["aliases"]} == {
            f"{sentinel_name}-alias-1",
            f"{sentinel_name}-alias-2",
        }
        # A new food is scoped to no household, so the seed below is a real
        # change and a clobber back to the default is visible.
        assert created["householdsWithIngredientFood"] == []

        seed = CreateIngredientFood.from_dict(created)
        seed.additional_properties = {}
        extras_seed = CreateIngredientFoodExtrasType0()
        extras_seed[SEED_EXTRAS_KEY] = f"{sentinel_name}-extras"
        seed.extras = extras_seed
        seed.households_with_ingredient_food = [household_slug]
        seeded = expect_dict(
            "seed_food_fields",
            update_one_api_foods_item_id_put.sync_detailed(
                item_id, client=mealie_client, body=seed
            ),
        )
        assert seeded["householdsWithIngredientFood"] == [household_slug]

        yield {
            "id": item_id,
            "name": sentinel_name,
            "label_id": sentinel_label,
            "household_slug": household_slug,
        }
    finally:
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=item_id)


@pytest.mark.live
def test_food_lifecycle(mealie_client: AuthenticatedClient, created_food: dict[str, str]) -> None:
    item_id = created_food["id"]
    name = created_food["name"]
    label_id = created_food["label_id"]
    households = [created_food["household_slug"]]

    seeded_aliases = {f"{name}-alias-1", f"{name}-alias-2"}

    fetched = recipes_foods.get_food(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == name
    assert fetched["pluralName"] == f"{name}-plural"
    assert fetched["description"] == f"{name}-description"
    assert {alias["name"] for alias in fetched["aliases"]} == seeded_aliases
    assert fetched["extras"][SEED_EXTRAS_KEY] == f"{name}-extras"
    assert fetched["householdsWithIngredientFood"] == households
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
    assert updated["householdsWithIngredientFood"] == households
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
    assert updated["householdsWithIngredientFood"] == households
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
def test_update_food_empty_values_clear_text_and_aliases(
    mealie_client: AuthenticatedClient, created_food: dict[str, str]
) -> None:
    item_id = created_food["id"]
    # An empty string clears the plural name and description and an empty list
    # clears the aliases, rather than being skipped the way an omitted (None)
    # field is.
    updated = recipes_foods.update_food(
        mealie_client, item_id=item_id, plural_name="", description="", aliases=[]
    )
    assert updated["pluralName"] == ""
    assert updated["description"] == ""
    assert updated["aliases"] == []
    refetched = recipes_foods.get_food(mealie_client, item_id=item_id)
    assert refetched["pluralName"] == ""
    assert refetched["description"] == ""
    assert refetched["aliases"] == []


@pytest.mark.live
def test_update_food_detaches_and_reattaches_the_label(
    mealie_client: AuthenticatedClient, created_food: dict[str, str]
) -> None:
    item_id = created_food["id"]
    label_id = created_food["label_id"]

    cleared = recipes_foods.update_food(mealie_client, item_id=item_id, label_id="")
    assert cleared["labelId"] is None
    assert cleared["label"] is None
    assert recipes_foods.get_food(mealie_client, item_id=item_id)["labelId"] is None

    reattached = recipes_foods.update_food(mealie_client, item_id=item_id, label_id=label_id)
    assert reattached["labelId"] == label_id
    assert recipes_foods.get_food(mealie_client, item_id=item_id)["labelId"] == label_id


@pytest.mark.live
def test_food_label_id_rejects_a_label_name(
    mealie_client: AuthenticatedClient, created_food: dict[str, str]
) -> None:
    """Both food tools document that `label_id` takes a UUID, not a label name."""
    name = created_food["name"]
    label_name = f"{name}-label"

    with pytest.raises(ToolError, match=r"Mealie create_food failed \(422"):
        recipes_foods.create_food(mealie_client, name=f"{name}-2", label_id=label_name)

    with pytest.raises(ToolError, match=r"Mealie update_food failed \(422"):
        recipes_foods.update_food(mealie_client, item_id=created_food["id"], label_id=label_name)


@pytest.mark.live
def test_create_food_round_trips_fields_through_wrapper(
    sentinel_name: str,
    sentinel_label: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    """The wrapper forwards the descriptive fields, aliases, and label to the tool."""
    created = call_tool(
        "mealie_create_food",
        {
            "name": sentinel_name,
            "plural_name": f"{sentinel_name}-plural",
            "description": f"{sentinel_name}-description",
            "aliases": [f"{sentinel_name}-alias"],
            "label_id": sentinel_label,
        },
    )
    assert isinstance(created, dict)
    item_id = str(created["id"])
    try:
        assert created["name"] == sentinel_name
        assert created["pluralName"] == f"{sentinel_name}-plural"
        assert created["description"] == f"{sentinel_name}-description"
        assert [alias["name"] for alias in created["aliases"]] == [f"{sentinel_name}-alias"]
        assert created["labelId"] == sentinel_label
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_food", {"item_id": item_id})


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
        assert fetched["labelId"] is None
    finally:
        with contextlib.suppress(ToolError):
            recipes_foods.delete_food(mealie_client, item_id=item_id)
