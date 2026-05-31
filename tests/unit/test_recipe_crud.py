"""Unit tests for the recipe CRUD tool implementations.

We pin the generated client to an `httpx.MockTransport` so the pure logic
(argument validation, status handling, error mapping) is exercised without any
network access.
"""

from __future__ import annotations

import json
from collections.abc import Iterable

import httpx
import pytest
from fastmcp.exceptions import ToolError

from mealie_mcp.client.client import AuthenticatedClient
from mealie_mcp.tools import recipe_crud


def _mock_client(handler: httpx.MockTransport) -> AuthenticatedClient:
    client = AuthenticatedClient(base_url="https://mealie.example.com", token="t")
    client.set_httpx_client(httpx.Client(transport=handler, base_url="https://mealie.example.com"))
    return client


def _responder(routes: Iterable[tuple[str, str, httpx.Response]]) -> httpx.MockTransport:
    routes_list = list(routes)

    def handler(request: httpx.Request) -> httpx.Response:
        for method, path, response in routes_list:
            if request.method == method and request.url.path == path:
                return response
        return httpx.Response(
            404, json={"detail": f"no route for {request.method} {request.url.path}"}
        )

    return httpx.MockTransport(handler)


class TestCreateRecipe:
    def test_rejects_empty_name(self) -> None:
        client = _mock_client(_responder([]))
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipe_crud.create_recipe(client, name="")

    def test_rejects_whitespace_name(self) -> None:
        client = _mock_client(_responder([]))
        with pytest.raises(ToolError, match="name must be a non-empty string"):
            recipe_crud.create_recipe(client, name="   ")

    def test_returns_slug_on_success(self) -> None:
        client = _mock_client(
            _responder([("POST", "/api/recipes", httpx.Response(201, json="my-recipe"))])
        )
        assert recipe_crud.create_recipe(client, name="My Recipe") == {"slug": "my-recipe"}

    def test_maps_api_error(self) -> None:
        client = _mock_client(
            _responder(
                [
                    (
                        "POST",
                        "/api/recipes",
                        httpx.Response(409, json={"detail": "Recipe already exists"}),
                    )
                ]
            )
        )
        with pytest.raises(ToolError, match=r"create_recipe failed \(409\): Recipe already exists"):
            recipe_crud.create_recipe(client, name="dupe")


class TestGetRecipe:
    def test_rejects_empty_slug(self) -> None:
        client = _mock_client(_responder([]))
        with pytest.raises(ToolError, match="slug_or_id must be a non-empty string"):
            recipe_crud.get_recipe(client, slug_or_id="")

    def test_returns_payload_on_success(self) -> None:
        payload = {"id": "abc", "slug": "my-recipe", "name": "My Recipe"}
        client = _mock_client(
            _responder([("GET", "/api/recipes/my-recipe", httpx.Response(200, json=payload))])
        )
        assert recipe_crud.get_recipe(client, slug_or_id="my-recipe") == payload

    def test_maps_not_found(self) -> None:
        client = _mock_client(
            _responder(
                [
                    (
                        "GET",
                        "/api/recipes/missing",
                        httpx.Response(404, json={"detail": "Not found."}),
                    )
                ]
            )
        )
        with pytest.raises(ToolError, match=r"get_recipe failed \(404\): Not found."):
            recipe_crud.get_recipe(client, slug_or_id="missing")


class TestDeleteRecipe:
    def test_rejects_empty_slug(self) -> None:
        client = _mock_client(_responder([]))
        with pytest.raises(ToolError, match="slug_or_id must be a non-empty string"):
            recipe_crud.delete_recipe(client, slug_or_id="")

    def test_returns_payload_on_success(self) -> None:
        payload = {"id": "abc", "slug": "my-recipe"}
        client = _mock_client(
            _responder([("DELETE", "/api/recipes/my-recipe", httpx.Response(200, json=payload))])
        )
        assert recipe_crud.delete_recipe(client, slug_or_id="my-recipe") == payload

    def test_maps_not_found(self) -> None:
        client = _mock_client(
            _responder(
                [
                    (
                        "DELETE",
                        "/api/recipes/missing",
                        httpx.Response(404, json={"detail": "Recipe not found"}),
                    )
                ]
            )
        )
        with pytest.raises(ToolError, match=r"delete_recipe failed \(404\): Recipe not found"):
            recipe_crud.delete_recipe(client, slug_or_id="missing")


class TestErrorBodyShapes:
    """The error-mapping helper should cope with non-dict bodies."""

    def test_string_body(self) -> None:
        client = _mock_client(
            _responder(
                [
                    (
                        "GET",
                        "/api/recipes/x",
                        httpx.Response(
                            500, content=b"upstream boom", headers={"content-type": "text/plain"}
                        ),
                    )
                ]
            )
        )
        with pytest.raises(ToolError, match=r"get_recipe failed \(500\): upstream boom"):
            recipe_crud.get_recipe(client, slug_or_id="x")

    def test_empty_body(self) -> None:
        client = _mock_client(_responder([("GET", "/api/recipes/x", httpx.Response(502))]))
        with pytest.raises(ToolError, match=r"get_recipe failed \(502\): HTTP 502"):
            recipe_crud.get_recipe(client, slug_or_id="x")

    def test_nested_detail_dict(self) -> None:
        body = {"detail": {"code": "conflict", "message": "Slug taken"}}
        client = _mock_client(
            _responder([("POST", "/api/recipes", httpx.Response(409, json=body))])
        )
        with pytest.raises(ToolError) as excinfo:
            recipe_crud.create_recipe(client, name="x")
        message = str(excinfo.value)
        assert "create_recipe failed (409):" in message
        assert json.loads(message.split("): ", 1)[1]) == body["detail"]
