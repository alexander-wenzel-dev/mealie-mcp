"""Live test for the unit lifecycle.

Stages a sentinel unit, exercises the read, list, update, and delete tools,
and tears the sentinel down even when the body fails so no `mcp-test-`
data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.api.recipes_units import update_one_api_units_item_id_put
from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.client.models.create_ingredient_unit import CreateIngredientUnit
from mealie_mcp.tools import recipes_units
from mealie_mcp.tools._common import expect_dict

SEED_STANDARD_QUANTITY = 2.5


@pytest.fixture
def created_unit(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> Iterator[dict[str, str]]:
    """Stage a sentinel unit via `create_unit`, then seed unexposed fields.

    Staging through the tool gives `create_unit` live coverage for the
    descriptive fields, with both booleans set to their non-default values.
    `description`, `standard_quantity`, and `standard_unit` are body-model
    fields the unit tools do not expose, so they are the ones a naive PUT
    would silently clobber. They are seeded with a direct PUT built from the
    created payload, so an update that touches only exposed fields must leave
    them intact. `extras` is not used as a seed because Mealie accepts it on
    the unit PUT but does not persist it, and `standard_quantity` only
    persists when the same body carries a non-null `standard_unit`.
    """
    created = recipes_units.create_unit(
        mealie_client,
        name=sentinel_name,
        abbreviation=f"{sentinel_name}-abbr",
        plural_name=f"{sentinel_name}-plural",
        plural_abbreviation=f"{sentinel_name}-plural-abbr",
        use_abbreviation=True,
        fraction=False,
        aliases=[f"{sentinel_name}-alias-1", f"{sentinel_name}-alias-2"],
    )
    item_id = str(created["id"])
    try:
        assert created["name"] == sentinel_name
        assert created["abbreviation"] == f"{sentinel_name}-abbr"
        assert created["pluralName"] == f"{sentinel_name}-plural"
        assert created["pluralAbbreviation"] == f"{sentinel_name}-plural-abbr"
        assert created["useAbbreviation"] is True
        assert created["fraction"] is False
        assert {alias["name"] for alias in created["aliases"]} == {
            f"{sentinel_name}-alias-1",
            f"{sentinel_name}-alias-2",
        }

        seed = CreateIngredientUnit.from_dict(created)
        seed.additional_properties = {}
        seed.description = f"{sentinel_name}-description"
        seed.standard_quantity = SEED_STANDARD_QUANTITY
        seed.standard_unit = f"{sentinel_name}-std-unit"
        expect_dict(
            "seed_unit_fields",
            update_one_api_units_item_id_put.sync_detailed(
                item_id, client=mealie_client, body=seed
            ),
        )

        yield {"id": item_id, "name": sentinel_name}
    finally:
        with contextlib.suppress(ToolError):
            recipes_units.delete_unit(mealie_client, item_id=item_id)


@pytest.mark.live
def test_unit_lifecycle(mealie_client: AuthenticatedClient, created_unit: dict[str, str]) -> None:
    item_id = created_unit["id"]
    name = created_unit["name"]

    seeded_aliases = {f"{name}-alias-1", f"{name}-alias-2"}

    fetched = recipes_units.get_unit(mealie_client, item_id=item_id)
    assert fetched["id"] == item_id
    assert fetched["name"] == name
    assert fetched["abbreviation"] == f"{name}-abbr"
    assert fetched["pluralName"] == f"{name}-plural"
    assert fetched["pluralAbbreviation"] == f"{name}-plural-abbr"
    assert fetched["useAbbreviation"] is True
    assert fetched["fraction"] is False
    assert {alias["name"] for alias in fetched["aliases"]} == seeded_aliases
    assert fetched["description"] == f"{name}-description"
    assert fetched["standardQuantity"] == SEED_STANDARD_QUANTITY
    assert fetched["standardUnit"] == f"{name}-std-unit"

    listing = recipes_units.list_units(mealie_client, search=name, per_page=100)
    assert any(u["id"] == item_id for u in listing["items"])

    renamed = f"{name}-renamed"
    updated = recipes_units.update_unit(mealie_client, item_id=item_id, name=renamed)
    assert updated["id"] == item_id
    assert updated["name"] == renamed
    assert updated["abbreviation"] == f"{name}-abbr"
    assert updated["pluralName"] == f"{name}-plural"
    assert updated["pluralAbbreviation"] == f"{name}-plural-abbr"
    assert updated["useAbbreviation"] is True
    assert updated["fraction"] is False
    assert {alias["name"] for alias in updated["aliases"]} == seeded_aliases
    assert updated["description"] == f"{name}-description"
    assert updated["standardQuantity"] == SEED_STANDARD_QUANTITY
    assert updated["standardUnit"] == f"{name}-std-unit"

    updated = recipes_units.update_unit(
        mealie_client,
        item_id=item_id,
        abbreviation=f"{name}-abbr-2",
        use_abbreviation=False,
        aliases=[f"{name}-alias-3"],
    )
    assert updated["name"] == renamed
    assert updated["abbreviation"] == f"{name}-abbr-2"
    assert updated["useAbbreviation"] is False
    assert {alias["name"] for alias in updated["aliases"]} == {f"{name}-alias-3"}
    assert updated["pluralName"] == f"{name}-plural"
    assert updated["pluralAbbreviation"] == f"{name}-plural-abbr"
    assert updated["fraction"] is False
    assert updated["description"] == f"{name}-description"
    assert updated["standardQuantity"] == SEED_STANDARD_QUANTITY
    assert updated["standardUnit"] == f"{name}-std-unit"

    refetched = recipes_units.get_unit(mealie_client, item_id=item_id)
    assert refetched["abbreviation"] == f"{name}-abbr-2"
    assert refetched["useAbbreviation"] is False
    assert {alias["name"] for alias in refetched["aliases"]} == {f"{name}-alias-3"}

    ack = recipes_units.delete_unit(mealie_client, item_id=item_id)
    assert ack == {"id": item_id, "deleted": True}

    with pytest.raises(ToolError, match=r"Mealie get_unit failed \(404"):
        recipes_units.get_unit(mealie_client, item_id=item_id)


@pytest.mark.live
def test_create_unit_name_only_leaves_defaults(
    mealie_client: AuthenticatedClient, sentinel_name: str
) -> None:
    """A name-only create sends no optional fields, so Mealie's defaults apply."""
    created = recipes_units.create_unit(mealie_client, name=sentinel_name)
    item_id = str(created["id"])
    try:
        fetched = recipes_units.get_unit(mealie_client, item_id=item_id)
        assert fetched["abbreviation"] == ""
        assert fetched["useAbbreviation"] is False
        assert fetched["fraction"] is True
        assert fetched["aliases"] == []
    finally:
        with contextlib.suppress(ToolError):
            recipes_units.delete_unit(mealie_client, item_id=item_id)
