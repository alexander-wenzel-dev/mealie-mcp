"""Live test for the household shopping list lifecycle.

Stages a sentinel shopping list, exercises the get, list, rename, and delete
tools, and asserts the rename preserves the list's items and extras. Two items
and an extras key are seeded before the rename, so a regression in
fetch-then-merge would clobber either ``listItems`` or ``extras`` on the
PUT-replace and fail the test. Cleanup runs even when the body fails so no
`mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.households_shopping_lists import (
    update_one_api_households_shopping_lists_item_id_put,
)
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.shopping_list_update import ShoppingListUpdate
from mealie_mcp.client.models.shopping_list_update_extras_type_0 import (
    ShoppingListUpdateExtrasType0,
)
from mealie_mcp.tools import households_shopping_list_items, households_shopping_lists, recipe_crud
from mealie_mcp.tools._common import expect_dict


@pytest.fixture
def created_shopping_list(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Create a sentinel shopping list and tear it down."""
    created = households_shopping_lists.create_shopping_list(mealie_client, name=sentinel_name)
    list_id = created["id"]
    try:
        yield {"id": list_id}
    finally:
        with contextlib.suppress(ToolError):
            households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)


def _seed_extras(client: AuthenticatedClient, list_id: str, *, key: str, value: str) -> None:
    """Set a non-default ``extras`` entry on a list via a direct PUT.

    ``extras`` is not exposed by ``update_shopping_list``, so a naive PUT would
    overwrite it. Seeding it here lets the lifecycle test assert it survives the
    rename, alongside the seeded items.
    """
    fetched = households_shopping_lists.get_shopping_list(client, list_id=list_id)
    extras_seed = ShoppingListUpdateExtrasType0()
    extras_seed[key] = value
    body = ShoppingListUpdate(
        group_id=fetched["groupId"],
        user_id=fetched["userId"],
        id=list_id,
        name=fetched["name"],
        extras=extras_seed,
    )
    expect_dict(
        "seed_extras",
        update_one_api_households_shopping_lists_item_id_put.sync_detailed(
            list_id, client=client, body=body
        ),
    )


@pytest.mark.live
def test_shopping_list_lifecycle(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]

    fetched = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert fetched["id"] == list_id
    assert fetched["name"] == sentinel_name

    listing = households_shopping_lists.list_shopping_lists(mealie_client, per_page=100)
    assert any(item["id"] == list_id for item in listing["items"])

    # Seed two unexposed body-model fields: extras (via a direct PUT on the
    # list endpoint) and listItems (via the dedicated items endpoint, which is
    # a separate POST and does not touch the list body). A merge regression on
    # either during the rename would fail below.
    extras_key = f"extras_{sentinel_name.replace('-', '_')}"
    extras_value = f"{sentinel_name}-extras"
    _seed_extras(mealie_client, list_id, key=extras_key, value=extras_value)
    first = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-a"
    )
    second = households_shopping_list_items.add_shopping_list_item(
        mealie_client, shopping_list_id=list_id, note=f"{sentinel_name}-b"
    )

    new_name = f"{sentinel_name}-renamed"
    renamed = households_shopping_lists.update_shopping_list(
        mealie_client, list_id=list_id, name=new_name
    )
    assert renamed["name"] == new_name

    after = households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)
    assert after["name"] == new_name
    surviving = {item["id"]: item for item in after["listItems"]}
    assert first["id"] in surviving
    assert second["id"] in surviving
    # The items keep their notes, not just their ids: a merge that reset item
    # fields while preserving ids would still fail here.
    assert surviving[first["id"]]["note"] == f"{sentinel_name}-a"
    assert surviving[second["id"]]["note"] == f"{sentinel_name}-b"
    assert after["extras"][extras_key] == extras_value

    ack = households_shopping_lists.delete_shopping_list(mealie_client, list_id=list_id)
    assert ack == {"id": list_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_shopping_list failed \(404"):
        households_shopping_lists.get_shopping_list(mealie_client, list_id=list_id)


def _staged_recipe(
    client: AuthenticatedClient, sentinel_name: str, *, suffix: str
) -> tuple[str, str]:
    """Create a sentinel recipe with one ingredient. Returns ``(slug, recipe_id)``."""
    slug = recipe_crud.create_recipe(client, name=f"{sentinel_name}-{suffix}")["slug"]
    recipe_crud.update_recipe(
        client,
        slug_or_id=slug,
        recipe_ingredient=[{"note": f"{sentinel_name}-{suffix}-ing"}],
    )
    recipe_id = recipe_crud.get_recipe(client, slug_or_id=slug)["id"]
    return slug, recipe_id


def _recipe_ref(shopping_list: dict[str, object], recipe_id: str) -> dict[str, object] | None:
    """The shopping list's recipe reference for ``recipe_id``, or ``None``."""
    references = shopping_list["recipeReferences"]
    assert isinstance(references, list)
    return next((ref for ref in references if ref["recipeId"] == recipe_id), None)


@pytest.mark.live
def test_add_recipe_to_list_scales_reference(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    slug, recipe_id = _staged_recipe(mealie_client, sentinel_name, suffix="single")
    try:
        updated = households_shopping_lists.add_recipe_to_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id, scale=2.0
        )
        # The recipe lands on the list as both a reference and concrete items.
        ref = _recipe_ref(updated, recipe_id)
        assert ref is not None, f"recipe {recipe_id} not referenced after add"
        # scale=2.0 rides through to the reference quantity, not the default 1.0.
        assert ref["recipeQuantity"] == 2.0
        assert isinstance(updated["listItems"], list)
        assert len(updated["listItems"]) >= 1
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_add_recipes_to_list_adds_each_with_its_scale(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    first_slug, first_id = _staged_recipe(mealie_client, sentinel_name, suffix="bulk-a")
    second_slug, second_id = _staged_recipe(mealie_client, sentinel_name, suffix="bulk-b")
    try:
        updated = households_shopping_lists.add_recipes_to_shopping_list(
            mealie_client,
            list_id=list_id,
            recipes=[
                {"recipe_id": first_id},
                {"recipe_id": second_id, "scale": 3.0},
            ],
        )
        first_ref = _recipe_ref(updated, first_id)
        second_ref = _recipe_ref(updated, second_id)
        assert first_ref is not None, f"recipe {first_id} not referenced after bulk add"
        assert second_ref is not None, f"recipe {second_id} not referenced after bulk add"
        # Per-entry scale is honoured independently: default 1.0 vs explicit 3.0.
        assert first_ref["recipeQuantity"] == 1.0
        assert second_ref["recipeQuantity"] == 3.0
    finally:
        for slug in (first_slug, second_slug):
            with contextlib.suppress(ToolError):
                recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_add_recipe_scales_item_quantities(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    note = f"{sentinel_name}-eggs"
    slug = recipe_crud.create_recipe(mealie_client, name=f"{sentinel_name}-qty")["slug"]
    recipe_crud.update_recipe(
        mealie_client, slug_or_id=slug, recipe_ingredient=[{"quantity": 3, "note": note}]
    )
    recipe_id = recipe_crud.get_recipe(mealie_client, slug_or_id=slug)["id"]
    try:
        updated = households_shopping_lists.add_recipe_to_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id, scale=2.0
        )
        item = next((i for i in updated["listItems"] if i["note"] == note), None)
        assert item is not None, "recipe ingredient did not land as a list item"
        # scale=2.0 multiplies the ingredient quantity 3 into a list item of 6,
        # not just the recipe reference quantity.
        assert item["quantity"] == 6
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_remove_recipe_from_list_drops_reference(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    slug, recipe_id = _staged_recipe(mealie_client, sentinel_name, suffix="remove")
    try:
        added = households_shopping_lists.add_recipe_to_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id
        )
        assert _recipe_ref(added, recipe_id) is not None, "recipe missing after add"

        removed = households_shopping_lists.remove_recipe_from_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id
        )
        # Removing the full amount that was added drops the reference entirely.
        assert _recipe_ref(removed, recipe_id) is None
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_remove_recipe_from_list_decrements_reference(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    slug, recipe_id = _staged_recipe(mealie_client, sentinel_name, suffix="decrement")
    try:
        added = households_shopping_lists.add_recipe_to_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id, scale=2.0
        )
        added_ref = _recipe_ref(added, recipe_id)
        assert added_ref is not None, "recipe missing after add"
        assert added_ref["recipeQuantity"] == 2.0

        removed = households_shopping_lists.remove_recipe_from_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id, scale=1.0
        )
        # Removing less than was added keeps the reference and decrements its
        # quantity by the removed amount, rather than dropping it.
        remaining_ref = _recipe_ref(removed, recipe_id)
        assert remaining_ref is not None, "reference dropped on partial removal"
        assert remaining_ref["recipeQuantity"] == 1.0
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)


@pytest.mark.live
def test_update_shopping_list_rename_keeps_recipe_references(
    mealie_client: AuthenticatedClient,
    created_shopping_list: dict[str, str],
    sentinel_name: str,
) -> None:
    list_id = created_shopping_list["id"]
    slug, recipe_id = _staged_recipe(mealie_client, sentinel_name, suffix="rename-ref")
    try:
        households_shopping_lists.add_recipe_to_shopping_list(
            mealie_client, list_id=list_id, recipe_id=recipe_id
        )
        renamed = households_shopping_lists.update_shopping_list(
            mealie_client, list_id=list_id, name=f"{sentinel_name}-renamed"
        )
        assert renamed["name"] == f"{sentinel_name}-renamed"
        # A name-only update must not clobber the recipe link: fetch-then-merge
        # carries recipeReferences through the PUT-replace.
        assert _recipe_ref(renamed, recipe_id) is not None, "recipe reference dropped on rename"
    finally:
        with contextlib.suppress(ToolError):
            recipe_crud.delete_recipe(mealie_client, slug_or_id=slug)
