from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.scrape_recipe_data import ScrapeRecipeData
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ScrapeRecipeData,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/recipes/create/html-or-json",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | str | None:
    if response.status_code == 201:
        response_201 = cast(str, response.json())
        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ScrapeRecipeData,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | str]:
    """Create Recipe From Html Or Json

     Takes in raw HTML or a https://schema.org/Recipe object as a JSON string and parses it like a URL

    Args:
        accept_language (None | str | Unset):
        body (ScrapeRecipeData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | str]
    """

    kwargs = _get_kwargs(
        body=body,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ScrapeRecipeData,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | str | None:
    """Create Recipe From Html Or Json

     Takes in raw HTML or a https://schema.org/Recipe object as a JSON string and parses it like a URL

    Args:
        accept_language (None | str | Unset):
        body (ScrapeRecipeData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | str
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ScrapeRecipeData,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | str]:
    """Create Recipe From Html Or Json

     Takes in raw HTML or a https://schema.org/Recipe object as a JSON string and parses it like a URL

    Args:
        accept_language (None | str | Unset):
        body (ScrapeRecipeData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | str]
    """

    kwargs = _get_kwargs(
        body=body,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ScrapeRecipeData,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | str | None:
    """Create Recipe From Html Or Json

     Takes in raw HTML or a https://schema.org/Recipe object as a JSON string and parses it like a URL

    Args:
        accept_language (None | str | Unset):
        body (ScrapeRecipeData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
