from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.household_recipe_summary import HouseholdRecipeSummary
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    recipe_slug: str,
    *,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/households/self/recipes/{recipe_slug}".format(
            recipe_slug=quote(str(recipe_slug), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | HouseholdRecipeSummary | None:
    if response.status_code == 200:
        response_200 = HouseholdRecipeSummary.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | HouseholdRecipeSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recipe_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | HouseholdRecipeSummary]:
    """Get Household Recipe

     Returns recipe data for the current household

    Args:
        recipe_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HouseholdRecipeSummary]
    """

    kwargs = _get_kwargs(
        recipe_slug=recipe_slug,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recipe_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | HouseholdRecipeSummary | None:
    """Get Household Recipe

     Returns recipe data for the current household

    Args:
        recipe_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HouseholdRecipeSummary
    """

    return sync_detailed(
        recipe_slug=recipe_slug,
        client=client,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    recipe_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | HouseholdRecipeSummary]:
    """Get Household Recipe

     Returns recipe data for the current household

    Args:
        recipe_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | HouseholdRecipeSummary]
    """

    kwargs = _get_kwargs(
        recipe_slug=recipe_slug,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recipe_slug: str,
    *,
    client: AuthenticatedClient,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | HouseholdRecipeSummary | None:
    """Get Household Recipe

     Returns recipe data for the current household

    Args:
        recipe_slug (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | HouseholdRecipeSummary
    """

    return (
        await asyncio_detailed(
            recipe_slug=recipe_slug,
            client=client,
            accept_language=accept_language,
        )
    ).parsed
