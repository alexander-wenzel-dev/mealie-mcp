from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_start_data_migration_api_groups_migrations_post import (
    BodyStartDataMigrationApiGroupsMigrationsPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...models.report_summary import ReportSummary
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodyStartDataMigrationApiGroupsMigrationsPost,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/groups/migrations",
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ReportSummary | None:
    if response.status_code == 200:
        response_200 = ReportSummary.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ReportSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyStartDataMigrationApiGroupsMigrationsPost,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReportSummary]:
    """Start Data Migration

    Args:
        accept_language (None | str | Unset):
        body (BodyStartDataMigrationApiGroupsMigrationsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReportSummary]
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
    body: BodyStartDataMigrationApiGroupsMigrationsPost,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ReportSummary | None:
    """Start Data Migration

    Args:
        accept_language (None | str | Unset):
        body (BodyStartDataMigrationApiGroupsMigrationsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReportSummary
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyStartDataMigrationApiGroupsMigrationsPost,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReportSummary]:
    """Start Data Migration

    Args:
        accept_language (None | str | Unset):
        body (BodyStartDataMigrationApiGroupsMigrationsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReportSummary]
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
    body: BodyStartDataMigrationApiGroupsMigrationsPost,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ReportSummary | None:
    """Start Data Migration

    Args:
        accept_language (None | str | Unset):
        body (BodyStartDataMigrationApiGroupsMigrationsPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReportSummary
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
