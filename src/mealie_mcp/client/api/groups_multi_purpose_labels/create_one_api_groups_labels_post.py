from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.multi_purpose_label_create import MultiPurposeLabelCreate
from ...models.multi_purpose_label_out import MultiPurposeLabelOut
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: MultiPurposeLabelCreate,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/groups/labels",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | MultiPurposeLabelOut | None:
    if response.status_code == 200:
        response_200 = MultiPurposeLabelOut.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | MultiPurposeLabelOut]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: MultiPurposeLabelCreate,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | MultiPurposeLabelOut]:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (MultiPurposeLabelCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MultiPurposeLabelOut]
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
    body: MultiPurposeLabelCreate,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | MultiPurposeLabelOut | None:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (MultiPurposeLabelCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MultiPurposeLabelOut
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: MultiPurposeLabelCreate,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | MultiPurposeLabelOut]:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (MultiPurposeLabelCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | MultiPurposeLabelOut]
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
    body: MultiPurposeLabelCreate,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | MultiPurposeLabelOut | None:
    """Create One

    Args:
        accept_language (None | str | Unset):
        body (MultiPurposeLabelCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | MultiPurposeLabelOut
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
