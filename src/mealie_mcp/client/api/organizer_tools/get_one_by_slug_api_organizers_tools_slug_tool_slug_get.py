from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.tool_with_recipes import ToolWithRecipes
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tool_slug: str,
    *,
    accept_language: str | Unset | None = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/organizers/tools/slug/{tool_slug}".format(
            tool_slug=quote(str(tool_slug), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ToolWithRecipes | None:
    if response.status_code == 200:
        response_200 = ToolWithRecipes.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ToolWithRecipes]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tool_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: str | Unset | None = UNSET,
) -> Response[HTTPValidationError | ToolWithRecipes]:
    """Get One By Slug

    Args:
        tool_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ToolWithRecipes]
    """

    kwargs = _get_kwargs(
        tool_slug=tool_slug,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tool_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: str | Unset | None = UNSET,
) -> HTTPValidationError | ToolWithRecipes | None:
    """Get One By Slug

    Args:
        tool_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ToolWithRecipes
    """

    return sync_detailed(
        tool_slug=tool_slug,
        client=client,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    tool_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: str | Unset | None = UNSET,
) -> Response[HTTPValidationError | ToolWithRecipes]:
    """Get One By Slug

    Args:
        tool_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ToolWithRecipes]
    """

    kwargs = _get_kwargs(
        tool_slug=tool_slug,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tool_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: str | Unset | None = UNSET,
) -> HTTPValidationError | ToolWithRecipes | None:
    """Get One By Slug

    Args:
        tool_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ToolWithRecipes
    """

    return (
        await asyncio_detailed(
            tool_slug=tool_slug,
            client=client,
            accept_language=accept_language,
        )
    ).parsed
