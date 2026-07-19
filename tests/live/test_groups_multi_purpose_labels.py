"""Live tests for the multi purpose label lifecycle.

Stages a sentinel label and exercises create, get, list, update, and delete. The
lifecycle test proves a non-default ``color`` round-trips on create and survives
a name-only update, the clobber proof for the update tool's fetch-then-merge:
``color`` is absent from a name-only PUT body, so a sparse update would reset it
to Mealie's ``#959595`` default. Cleanup runs even when the body fails so no
`mcp-test-` data lingers.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import groups_multi_purpose_labels


@pytest.mark.live
def test_label_lifecycle_color_survives_name_only_update(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    color = "#123456"
    item_id: str | None = None
    try:
        created = groups_multi_purpose_labels.create_label(
            mealie_client, name=sentinel_name, color=color
        )
        item_id = created["id"]

        fetched = groups_multi_purpose_labels.get_label(mealie_client, item_id=item_id)
        assert fetched["name"] == sentinel_name
        assert fetched["color"] == color

        listing = groups_multi_purpose_labels.list_labels(mealie_client, per_page=100)
        assert any(item["id"] == item_id for item in listing["items"])

        new_name = f"{sentinel_name}-renamed"
        updated = groups_multi_purpose_labels.update_label(
            mealie_client, item_id=item_id, name=new_name
        )
        assert updated["name"] == new_name

        # A name-only update must not clobber the non-default color: fetch-then-merge
        # preserves it through the PUT-replace instead of resetting it to #959595.
        refetched = groups_multi_purpose_labels.get_label(mealie_client, item_id=item_id)
        assert refetched["name"] == new_name
        assert refetched["color"] == color

        ack = groups_multi_purpose_labels.delete_label(mealie_client, item_id=item_id)
        assert ack == {"id": item_id, "deleted": True}
        deleted_id, item_id = item_id, None

        # A get on a deleted label is gone: Mealie's labels endpoint answers a
        # valid but absent id with a 500 rather than the 404 the cookbook and tag
        # endpoints return, so the delete is proven by the tool raising, not by a
        # specific status.
        with pytest.raises(ToolError, match=r"Mealie get_label failed \(500"):
            groups_multi_purpose_labels.get_label(mealie_client, item_id=deleted_id)
    finally:
        if item_id is not None:
            with contextlib.suppress(ToolError):
                groups_multi_purpose_labels.delete_label(mealie_client, item_id=item_id)


@pytest.mark.live
def test_create_label_defaults_color_to_gray(
    mealie_client: AuthenticatedClient,
    sentinel_name: str,
) -> None:
    created = groups_multi_purpose_labels.create_label(mealie_client, name=sentinel_name)
    item_id = created["id"]
    try:
        # With color omitted, Mealie seeds the documented #959595 default rather
        # than leaving it empty.
        assert created["color"] == "#959595"
        fetched = groups_multi_purpose_labels.get_label(mealie_client, item_id=item_id)
        assert fetched["color"] == "#959595"
    finally:
        with contextlib.suppress(ToolError):
            groups_multi_purpose_labels.delete_label(mealie_client, item_id=item_id)


@pytest.mark.live
@pytest.mark.usefixtures("mealie_client")
def test_create_label_round_trips_color_through_wrapper(
    sentinel_name: str,
    call_tool: Callable[[str, dict[str, object]], object],
) -> None:
    color = "#abcdef"
    created = call_tool("mealie_create_label", {"name": sentinel_name, "color": color})
    assert isinstance(created, dict)
    item_id = created["id"]
    try:
        # name and color are both str; fetching both back catches a wrapper swap.
        fetched = call_tool("mealie_get_label", {"item_id": item_id})
        assert isinstance(fetched, dict)
        assert fetched["name"] == sentinel_name
        assert fetched["color"] == color
    finally:
        with contextlib.suppress(ToolError):
            call_tool("mealie_delete_label", {"item_id": item_id})
