from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.long_live_token_create_response import LongLiveTokenCreateResponse
from ...models.long_live_token_in import LongLiveTokenIn
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: LongLiveTokenIn,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/users/api-tokens",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | LongLiveTokenCreateResponse | None:
    if response.status_code == 201:
        response_201 = LongLiveTokenCreateResponse.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | LongLiveTokenCreateResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LongLiveTokenIn,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | LongLiveTokenCreateResponse]:
    """Create Api Token

     Create api_token in the Database

    Args:
        accept_language (None | str | Unset):
        body (LongLiveTokenIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LongLiveTokenCreateResponse]
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
    body: LongLiveTokenIn,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | LongLiveTokenCreateResponse | None:
    """Create Api Token

     Create api_token in the Database

    Args:
        accept_language (None | str | Unset):
        body (LongLiveTokenIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LongLiveTokenCreateResponse
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LongLiveTokenIn,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | LongLiveTokenCreateResponse]:
    """Create Api Token

     Create api_token in the Database

    Args:
        accept_language (None | str | Unset):
        body (LongLiveTokenIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | LongLiveTokenCreateResponse]
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
    body: LongLiveTokenIn,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | LongLiveTokenCreateResponse | None:
    """Create Api Token

     Create api_token in the Database

    Args:
        accept_language (None | str | Unset):
        body (LongLiveTokenIn):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | LongLiveTokenCreateResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
