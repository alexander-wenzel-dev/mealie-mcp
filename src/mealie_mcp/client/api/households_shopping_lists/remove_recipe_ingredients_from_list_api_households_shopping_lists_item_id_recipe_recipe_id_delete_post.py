from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.shopping_list_out import ShoppingListOut
from ...models.shopping_list_remove_recipe_params import ShoppingListRemoveRecipeParams
from ...types import UNSET, Response, Unset


def _get_kwargs(
    item_id: str,
    recipe_id: str,
    *,
    body: None | ShoppingListRemoveRecipeParams | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/households/shopping/lists/{item_id}/recipe/{recipe_id}/delete".format(
            item_id=quote(str(item_id), safe=""),
            recipe_id=quote(str(recipe_id), safe=""),
        ),
    }

    if isinstance(body, ShoppingListRemoveRecipeParams):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ShoppingListOut | None:
    if response.status_code == 200:
        response_200 = ShoppingListOut.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ShoppingListOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    item_id: str,
    recipe_id: str,
    *,
    client: AuthenticatedClient,
    body: None | ShoppingListRemoveRecipeParams | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ShoppingListOut]:
    """Remove Recipe Ingredients From List

    Args:
        item_id (str):
        recipe_id (str):
        accept_language (None | str | Unset):
        body (None | ShoppingListRemoveRecipeParams | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ShoppingListOut]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        recipe_id=recipe_id,
        body=body,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    item_id: str,
    recipe_id: str,
    *,
    client: AuthenticatedClient,
    body: None | ShoppingListRemoveRecipeParams | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ShoppingListOut | None:
    """Remove Recipe Ingredients From List

    Args:
        item_id (str):
        recipe_id (str):
        accept_language (None | str | Unset):
        body (None | ShoppingListRemoveRecipeParams | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ShoppingListOut
    """

    return sync_detailed(
        item_id=item_id,
        recipe_id=recipe_id,
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    item_id: str,
    recipe_id: str,
    *,
    client: AuthenticatedClient,
    body: None | ShoppingListRemoveRecipeParams | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ShoppingListOut]:
    """Remove Recipe Ingredients From List

    Args:
        item_id (str):
        recipe_id (str):
        accept_language (None | str | Unset):
        body (None | ShoppingListRemoveRecipeParams | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ShoppingListOut]
    """

    kwargs = _get_kwargs(
        item_id=item_id,
        recipe_id=recipe_id,
        body=body,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    item_id: str,
    recipe_id: str,
    *,
    client: AuthenticatedClient,
    body: None | ShoppingListRemoveRecipeParams | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ShoppingListOut | None:
    """Remove Recipe Ingredients From List

    Args:
        item_id (str):
        recipe_id (str):
        accept_language (None | str | Unset):
        body (None | ShoppingListRemoveRecipeParams | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ShoppingListOut
    """

    return (
        await asyncio_detailed(
            item_id=item_id,
            recipe_id=recipe_id,
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
