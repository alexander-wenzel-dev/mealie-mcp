from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_random_entry import CreateRandomEntry
from ...models.http_validation_error import HTTPValidationError
from ...models.read_plan_entry import ReadPlanEntry
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CreateRandomEntry,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/households/mealplans/random",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ReadPlanEntry | None:
    if response.status_code == 200:
        response_200 = ReadPlanEntry.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ReadPlanEntry]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateRandomEntry,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReadPlanEntry]:
    """Create Random Meal

     `create_random_meal` is a route that provides the randomized functionality for mealplaners.
    It operates by following the rules set out in the household's mealplan settings. If no settings
    are set, it will return any random meal.

    Refer to the mealplan settings routes for more information on how rules can be applied
    to the random meal selector.

    Args:
        accept_language (None | str | Unset):
        body (CreateRandomEntry):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReadPlanEntry]
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
    body: CreateRandomEntry,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ReadPlanEntry | None:
    """Create Random Meal

     `create_random_meal` is a route that provides the randomized functionality for mealplaners.
    It operates by following the rules set out in the household's mealplan settings. If no settings
    are set, it will return any random meal.

    Refer to the mealplan settings routes for more information on how rules can be applied
    to the random meal selector.

    Args:
        accept_language (None | str | Unset):
        body (CreateRandomEntry):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReadPlanEntry
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateRandomEntry,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ReadPlanEntry]:
    """Create Random Meal

     `create_random_meal` is a route that provides the randomized functionality for mealplaners.
    It operates by following the rules set out in the household's mealplan settings. If no settings
    are set, it will return any random meal.

    Refer to the mealplan settings routes for more information on how rules can be applied
    to the random meal selector.

    Args:
        accept_language (None | str | Unset):
        body (CreateRandomEntry):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReadPlanEntry]
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
    body: CreateRandomEntry,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | ReadPlanEntry | None:
    """Create Random Meal

     `create_random_meal` is a route that provides the randomized functionality for mealplaners.
    It operates by following the rules set out in the household's mealplan settings. If no settings
    are set, it will return any random meal.

    Refer to the mealplan settings routes for more information on how rules can be applied
    to the random meal selector.

    Args:
        accept_language (None | str | Unset):
        body (CreateRandomEntry):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReadPlanEntry
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
