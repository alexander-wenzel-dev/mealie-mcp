from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_ingredient_unit import CreateIngredientUnit
from ...models.http_validation_error import HTTPValidationError
from ...models.ingredient_unit_output import IngredientUnitOutput
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CreateIngredientUnit,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/units",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | IngredientUnitOutput | None:
    if response.status_code == 201:
        response_201 = IngredientUnitOutput.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | IngredientUnitOutput]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateIngredientUnit,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | IngredientUnitOutput]:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (CreateIngredientUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | IngredientUnitOutput]
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
    body: CreateIngredientUnit,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | IngredientUnitOutput | None:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (CreateIngredientUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | IngredientUnitOutput
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateIngredientUnit,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | IngredientUnitOutput]:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (CreateIngredientUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | IngredientUnitOutput]
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
    body: CreateIngredientUnit,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | IngredientUnitOutput | None:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (CreateIngredientUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | IngredientUnitOutput
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
