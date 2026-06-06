from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.recipe_duplicate import RecipeDuplicate
from ...models.recipe_output import RecipeOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    slug: str,
    *,
    body: RecipeDuplicate,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/recipes/{slug}/duplicate".format(
            slug=quote(str(slug), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RecipeOutput | None:
    if response.status_code == 201:
        response_201 = RecipeOutput.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | RecipeOutput]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: RecipeDuplicate,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecipeOutput]:
    """Duplicate One

     Duplicates a recipe with a new custom name if given

    Args:
        slug (str):
        accept_language (None | str | Unset):
        body (RecipeDuplicate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecipeOutput]
    """

    kwargs = _get_kwargs(
        slug=slug,
        body=body,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: RecipeDuplicate,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | RecipeOutput | None:
    """Duplicate One

     Duplicates a recipe with a new custom name if given

    Args:
        slug (str):
        accept_language (None | str | Unset):
        body (RecipeDuplicate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecipeOutput
    """

    return sync_detailed(
        slug=slug,
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: RecipeDuplicate,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecipeOutput]:
    """Duplicate One

     Duplicates a recipe with a new custom name if given

    Args:
        slug (str):
        accept_language (None | str | Unset):
        body (RecipeDuplicate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecipeOutput]
    """

    kwargs = _get_kwargs(
        slug=slug,
        body=body,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
    body: RecipeDuplicate,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | RecipeOutput | None:
    """Duplicate One

     Duplicates a recipe with a new custom name if given

    Args:
        slug (str):
        accept_language (None | str | Unset):
        body (RecipeDuplicate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecipeOutput
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
