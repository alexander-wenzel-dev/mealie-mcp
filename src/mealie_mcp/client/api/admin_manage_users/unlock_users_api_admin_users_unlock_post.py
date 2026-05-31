from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.unlock_results import UnlockResults
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    force: bool | Unset = False,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

    params["force"] = force

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/users/unlock",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | UnlockResults | None:
    if response.status_code == 200:
        response_200 = UnlockResults.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | UnlockResults]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | UnlockResults]:
    """Unlock Users

    Args:
        force (bool | Unset):  Default: False.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UnlockResults]
    """

    kwargs = _get_kwargs(
        force=force,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | UnlockResults | None:
    """Unlock Users

    Args:
        force (bool | Unset):  Default: False.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UnlockResults
    """

    return sync_detailed(
        client=client,
        force=force,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | UnlockResults]:
    """Unlock Users

    Args:
        force (bool | Unset):  Default: False.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | UnlockResults]
    """

    kwargs = _get_kwargs(
        force=force,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    force: bool | Unset = False,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | UnlockResults | None:
    """Unlock Users

    Args:
        force (bool | Unset):  Default: False.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | UnlockResults
    """

    return (
        await asyncio_detailed(
            client=client,
            force=force,
            accept_language=accept_language,
        )
    ).parsed
