from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.shopping_list_item_update_bulk import ShoppingListItemUpdateBulk
from ...models.shopping_list_items_collection_out import ShoppingListItemsCollectionOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: list[ShoppingListItemUpdateBulk],
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/households/shopping/items",
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ShoppingListItemsCollectionOut | None:
    if response.status_code == 200:
        response_200 = ShoppingListItemsCollectionOut.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ShoppingListItemsCollectionOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: list[ShoppingListItemUpdateBulk],
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ShoppingListItemsCollectionOut]:
    """Update Many

    Args:
        accept_language (None | str | Unset):
        body (list[ShoppingListItemUpdateBulk]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ShoppingListItemsCollectionOut]
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
    body: list[ShoppingListItemUpdateBulk],
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ShoppingListItemsCollectionOut | None:
    """Update Many

    Args:
        accept_language (None | str | Unset):
        body (list[ShoppingListItemUpdateBulk]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ShoppingListItemsCollectionOut
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: list[ShoppingListItemUpdateBulk],
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ShoppingListItemsCollectionOut]:
    """Update Many

    Args:
        accept_language (None | str | Unset):
        body (list[ShoppingListItemUpdateBulk]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ShoppingListItemsCollectionOut]
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
    body: list[ShoppingListItemUpdateBulk],
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ShoppingListItemsCollectionOut | None:
    """Update Many

    Args:
        accept_language (None | str | Unset):
        body (list[ShoppingListItemUpdateBulk]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ShoppingListItemsCollectionOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
