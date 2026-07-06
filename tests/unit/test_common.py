"""Tests for the shared tool helpers."""

from __future__ import annotations

import json
from http import HTTPStatus

import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.models.order_direction import OrderDirection
from mealie_mcp.client.types import UNSET, Response
from mealie_mcp.tools._common import (
    MAX_PER_PAGE,
    ack_delete,
    decode,
    expect_dict,
    expect_list,
    expect_str,
    parse_order_direction,
    parse_recipe_uuid,
    raise_api_error,
    require_non_empty,
    require_pagination,
    to_unset,
)


def _response(status: HTTPStatus, content: bytes) -> Response[None]:
    return Response(status_code=status, content=content, headers={}, parsed=None)


class TestDecode:
    def test_empty_bytes_returns_none(self) -> None:
        assert decode(b"") is None

    def test_json_string(self) -> None:
        assert decode(b'"hello"') == "hello"

    def test_json_object(self) -> None:
        assert decode(b'{"k": 1}') == {"k": 1}

    def test_non_json_falls_back_to_utf8(self) -> None:
        assert decode(b"plain text") == "plain text"


class TestRaiseApiError:
    def test_dict_with_string_detail(self) -> None:
        body = json.dumps({"detail": "Recipe already exists"}).encode()
        with pytest.raises(
            ToolError, match=r"^Mealie action failed \(409\): Recipe already exists$"
        ):
            raise_api_error("action", 409, body)

    def test_dict_with_message_fallback(self) -> None:
        body = json.dumps({"message": "boom"}).encode()
        with pytest.raises(ToolError, match=r"^Mealie action failed \(500\): boom$"):
            raise_api_error("action", 500, body)

    def test_dict_with_nested_detail(self) -> None:
        body = json.dumps({"detail": {"code": "x", "message": "y"}}).encode()
        with pytest.raises(ToolError) as excinfo:
            raise_api_error("action", 409, body)
        message = str(excinfo.value)
        assert message.startswith("Mealie action failed (409): ")
        assert json.loads(message.split("): ", 1)[1]) == {"code": "x", "message": "y"}

    def test_string_body(self) -> None:
        with pytest.raises(ToolError, match=r"^Mealie action failed \(500\): upstream boom$"):
            raise_api_error("action", 500, b"upstream boom")

    def test_empty_body_uses_status(self) -> None:
        with pytest.raises(ToolError, match=r"^Mealie action failed \(502\): HTTP 502$"):
            raise_api_error("action", 502, b"")

    def test_html_body_passes_through(self) -> None:
        html = b"<html><body><h1>502 Bad Gateway</h1></body></html>"
        with pytest.raises(ToolError) as excinfo:
            raise_api_error("action", 502, html)
        assert str(excinfo.value) == (
            "Mealie action failed (502): <html><body><h1>502 Bad Gateway</h1></body></html>"
        )


class TestRequireNonEmpty:
    def test_rejects_empty_string(self) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            require_non_empty("name", "")

    def test_rejects_whitespace(self) -> None:
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            require_non_empty("name", "   ")

    def test_accepts_value(self) -> None:
        require_non_empty("name", "x")


class TestRequirePagination:
    def test_accepts_per_page_at_max(self) -> None:
        require_pagination(1, MAX_PER_PAGE)

    def test_accepts_per_page_at_floor(self) -> None:
        require_pagination(1, 1)

    def test_rejects_per_page_above_max(self) -> None:
        with pytest.raises(
            ToolError, match=rf"per_page must be between 1 and {MAX_PER_PAGE} \(got 250\)"
        ):
            require_pagination(1, 250)

    @pytest.mark.parametrize("per_page", [0, -1])
    def test_rejects_per_page_below_floor(self, per_page: int) -> None:
        with pytest.raises(
            ToolError, match=rf"per_page must be between 1 and {MAX_PER_PAGE} \(got {per_page}\)"
        ):
            require_pagination(1, per_page)

    @pytest.mark.parametrize("page", [0, -1])
    def test_rejects_page_below_one(self, page: int) -> None:
        with pytest.raises(ToolError, match=rf"page must be >= 1 \(got {page}\)"):
            require_pagination(page, 50)


class TestParseRecipeUuid:
    def test_parses_valid_uuid(self) -> None:
        assert (
            str(parse_recipe_uuid("11111111-1111-1111-1111-111111111111"))
            == "11111111-1111-1111-1111-111111111111"
        )

    def test_rejects_non_uuid(self) -> None:
        with pytest.raises(ToolError, match="recipe_id must be a recipe UUID"):
            parse_recipe_uuid('x" or true')


class TestExpectDict:
    def test_returns_dict_on_ok(self) -> None:
        assert expect_dict("act", _response(HTTPStatus.OK, b'{"k": 1}')) == {"k": 1}

    def test_accepts_custom_status(self) -> None:
        assert expect_dict("act", _response(HTTPStatus.CREATED, b"{}"), HTTPStatus.CREATED) == {}

    def test_raises_on_unexpected_status(self) -> None:
        with pytest.raises(ToolError, match=r"act failed \(404\)"):
            expect_dict("act", _response(HTTPStatus.NOT_FOUND, b'{"detail": "nope"}'))

    def test_raises_on_non_dict_body(self) -> None:
        with pytest.raises(ToolError, match="Unexpected act response"):
            expect_dict("act", _response(HTTPStatus.OK, b"[]"))


class TestExpectList:
    def test_returns_list_on_ok(self) -> None:
        assert expect_list("act", _response(HTTPStatus.OK, b"[1, 2]")) == [1, 2]

    def test_raises_on_non_list_body(self) -> None:
        with pytest.raises(ToolError, match="Unexpected act response"):
            expect_list("act", _response(HTTPStatus.OK, b'{"k": 1}'))


class TestExpectStr:
    def test_returns_string_on_ok(self) -> None:
        assert (
            expect_str("act", _response(HTTPStatus.CREATED, b'"slug"'), HTTPStatus.CREATED)
            == "slug"
        )

    def test_raises_on_non_string_body(self) -> None:
        with pytest.raises(ToolError, match="Unexpected act response"):
            expect_str("act", _response(HTTPStatus.OK, b"{}"))


class TestToUnset:
    def test_none_becomes_unset(self) -> None:
        assert to_unset(None) is UNSET

    def test_value_passes_through(self) -> None:
        assert to_unset("hello") == "hello"
        assert to_unset(["a", "b"]) == ["a", "b"]

    def test_empty_string_passes_through(self) -> None:
        assert to_unset("") == ""

    def test_zero_passes_through(self) -> None:
        assert to_unset(0) == 0


class TestAckDelete:
    def test_returns_canonical_ack_on_ok(self) -> None:
        assert ack_delete("delete_x", _response(HTTPStatus.OK, b""), "abc") == {
            "id": "abc",
            "deleted": True,
        }

    def test_ignores_response_body_shape(self) -> None:
        assert ack_delete("delete_x", _response(HTTPStatus.OK, b'"slug"'), "abc") == {
            "id": "abc",
            "deleted": True,
        }
        assert ack_delete("delete_x", _response(HTTPStatus.OK, b'{"k": 1}'), "abc") == {
            "id": "abc",
            "deleted": True,
        }

    def test_raises_on_non_ok(self) -> None:
        with pytest.raises(ToolError, match=r"Mealie delete_x failed \(404\)"):
            ack_delete("delete_x", _response(HTTPStatus.NOT_FOUND, b'{"detail": "nope"}'), "abc")


class TestParseOrderDirection:
    def test_none_returns_unset(self) -> None:
        assert parse_order_direction(None) is UNSET

    def test_asc(self) -> None:
        assert parse_order_direction("asc") is OrderDirection.ASC

    def test_desc(self) -> None:
        assert parse_order_direction("desc") is OrderDirection.DESC

    def test_invalid_raises_tool_error(self) -> None:
        with pytest.raises(ToolError, match="order_direction must be 'asc' or 'desc'"):
            parse_order_direction("sideways")
