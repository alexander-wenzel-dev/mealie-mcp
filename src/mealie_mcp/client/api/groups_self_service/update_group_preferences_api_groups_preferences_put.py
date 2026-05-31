from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.read_group_preferences import ReadGroupPreferences
from ...models.update_group_preferences import UpdateGroupPreferences
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: UpdateGroupPreferences,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/groups/preferences",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ReadGroupPreferences | None:
    if response.status_code == 200:
        response_200 = ReadGroupPreferences.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ReadGroupPreferences]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: UpdateGroupPreferences,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReadGroupPreferences]:
    """Update Group Preferences

    Args:
        accept_language (None | str | Unset):
        body (UpdateGroupPreferences):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReadGroupPreferences]
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
    body: UpdateGroupPreferences,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ReadGroupPreferences | None:
    """Update Group Preferences

    Args:
        accept_language (None | str | Unset):
        body (UpdateGroupPreferences):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReadGroupPreferences
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: UpdateGroupPreferences,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReadGroupPreferences]:
    """Update Group Preferences

    Args:
        accept_language (None | str | Unset):
        body (UpdateGroupPreferences):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReadGroupPreferences]
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
    body: UpdateGroupPreferences,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ReadGroupPreferences | None:
    """Update Group Preferences

    Args:
        accept_language (None | str | Unset):
        body (UpdateGroupPreferences):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReadGroupPreferences
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
