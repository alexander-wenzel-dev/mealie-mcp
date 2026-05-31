from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.report_category import ReportCategory
from ...models.report_summary import ReportSummary
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    report_type: None | ReportCategory | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

    json_report_type: None | str | Unset
    if isinstance(report_type, Unset):
        json_report_type = UNSET
    elif isinstance(report_type, ReportCategory):
        json_report_type = report_type.value
    else:
        json_report_type = report_type
    params["report_type"] = json_report_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/groups/reports",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | list[ReportSummary] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ReportSummary.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | list[ReportSummary]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    report_type: None | ReportCategory | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[ReportSummary]]:
    """Get All

    Args:
        report_type (None | ReportCategory | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ReportSummary]]
    """

    kwargs = _get_kwargs(
        report_type=report_type,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    report_type: None | ReportCategory | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | list[ReportSummary] | None:
    """Get All

    Args:
        report_type (None | ReportCategory | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ReportSummary]
    """

    return sync_detailed(
        client=client,
        report_type=report_type,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    report_type: None | ReportCategory | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | list[ReportSummary]]:
    """Get All

    Args:
        report_type (None | ReportCategory | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | list[ReportSummary]]
    """

    kwargs = _get_kwargs(
        report_type=report_type,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    report_type: None | ReportCategory | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | list[ReportSummary] | None:
    """Get All

    Args:
        report_type (None | ReportCategory | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | list[ReportSummary]
    """

    return (
        await asyncio_detailed(
            client=client,
            report_type=report_type,
            accept_language=accept_language,
        )
    ).parsed
