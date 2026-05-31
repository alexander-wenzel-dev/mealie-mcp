from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    category_slug: str,
    *,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/organizers/categories/slug/{category_slug}".format(
            category_slug=quote(str(category_slug), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    category_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get One By Slug

     Returns a category object with the associated recieps relating to the category

    Args:
        category_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_slug=category_slug,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    category_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Get One By Slug

     Returns a category object with the associated recieps relating to the category

    Args:
        category_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        category_slug=category_slug,
        client=client,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    category_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get One By Slug

     Returns a category object with the associated recieps relating to the category

    Args:
        category_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        category_slug=category_slug,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    category_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Get One By Slug

     Returns a category object with the associated recieps relating to the category

    Args:
        category_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            category_slug=category_slug,
            client=client,
            accept_language=accept_language,
        )
    ).parsed
