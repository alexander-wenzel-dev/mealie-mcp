from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.household_summary import HouseholdSummary
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    household_slug: str,
    *,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/groups/households/{household_slug}".format(
            household_slug=quote(str(household_slug), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | HouseholdSummary | None:
    if response.status_code == 200:
        response_200 = HouseholdSummary.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | HouseholdSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    household_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | HouseholdSummary]:
    """Get One Household

    Args:
        household_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HouseholdSummary]
    """

    kwargs = _get_kwargs(
        household_slug=household_slug,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    household_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | HouseholdSummary | None:
    """Get One Household

    Args:
        household_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HouseholdSummary
    """

    return sync_detailed(
        household_slug=household_slug,
        client=client,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    household_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | HouseholdSummary]:
    """Get One Household

    Args:
        household_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HouseholdSummary]
    """

    kwargs = _get_kwargs(
        household_slug=household_slug,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    household_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | HouseholdSummary | None:
    """Get One Household

    Args:
        household_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HouseholdSummary
    """

    return (
        await asyncio_detailed(
            household_slug=household_slug,
            client=client,
            accept_language=accept_language,
        )
    ).parsed
