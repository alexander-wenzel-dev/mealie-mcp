from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_debug_openai_api_admin_debug_openai_provider_id_post import (
    BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost,
)
from ...models.debug_response import DebugResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    provider_id: str,
    *,
    body: BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/debug/openai/{provider_id}".format(
            provider_id=quote(str(provider_id), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> DebugResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = DebugResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[DebugResponse | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[DebugResponse | HTTPValidationError]:
    """Debug Openai

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DebugResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        provider_id=provider_id,
        body=body,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> DebugResponse | HTTPValidationError | None:
    """Debug Openai

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DebugResponse | HTTPValidationError
    """

    return sync_detailed(
        provider_id=provider_id,
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[DebugResponse | HTTPValidationError]:
    """Debug Openai

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DebugResponse | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        provider_id=provider_id,
        body=body,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> DebugResponse | HTTPValidationError | None:
    """Debug Openai

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (BodyDebugOpenaiApiAdminDebugOpenaiProviderIdPost | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DebugResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            provider_id=provider_id,
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
