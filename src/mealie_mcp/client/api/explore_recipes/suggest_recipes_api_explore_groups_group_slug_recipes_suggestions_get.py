from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.order_by_null_position import OrderByNullPosition
from ...models.order_direction import OrderDirection
from ...models.recipe_suggestion_response import RecipeSuggestionResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_slug: str,
    *,
    foods: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    limit: int | Unset = 10,
    max_missing_foods: int | Unset = 5,
    max_missing_tools: int | Unset = 5,
    include_foods_on_hand: bool | Unset = True,
    include_tools_on_hand: bool | Unset = True,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

    json_foods: list[str] | None | Unset
    if isinstance(foods, Unset):
        json_foods = UNSET
    elif isinstance(foods, list):
        json_foods = foods

    else:
        json_foods = foods
    params["foods"] = json_foods

    json_tools: list[str] | None | Unset
    if isinstance(tools, Unset):
        json_tools = UNSET
    elif isinstance(tools, list):
        json_tools = tools

    else:
        json_tools = tools
    params["tools"] = json_tools

    json_order_by: None | str | Unset
    if isinstance(order_by, Unset):
        json_order_by = UNSET
    else:
        json_order_by = order_by
    params["orderBy"] = json_order_by

    json_order_by_null_position: None | str | Unset
    if isinstance(order_by_null_position, Unset):
        json_order_by_null_position = UNSET
    elif isinstance(order_by_null_position, OrderByNullPosition):
        json_order_by_null_position = order_by_null_position.value
    else:
        json_order_by_null_position = order_by_null_position
    params["orderByNullPosition"] = json_order_by_null_position

    json_order_direction: str | Unset = UNSET
    if not isinstance(order_direction, Unset):
        json_order_direction = order_direction.value

    params["orderDirection"] = json_order_direction

    json_query_filter: None | str | Unset
    if isinstance(query_filter, Unset):
        json_query_filter = UNSET
    else:
        json_query_filter = query_filter
    params["queryFilter"] = json_query_filter

    json_pagination_seed: None | str | Unset
    if isinstance(pagination_seed, Unset):
        json_pagination_seed = UNSET
    else:
        json_pagination_seed = pagination_seed
    params["paginationSeed"] = json_pagination_seed

    params["limit"] = limit

    params["maxMissingFoods"] = max_missing_foods

    params["maxMissingTools"] = max_missing_tools

    params["includeFoodsOnHand"] = include_foods_on_hand

    params["includeToolsOnHand"] = include_tools_on_hand

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/explore/groups/{group_slug}/recipes/suggestions".format(
            group_slug=quote(str(group_slug), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | RecipeSuggestionResponse | None:
    if response.status_code == 200:
        response_200 = RecipeSuggestionResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | RecipeSuggestionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_slug: str,
    *,
    client: AuthenticatedClient | Client,
    foods: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    limit: int | Unset = 10,
    max_missing_foods: int | Unset = 5,
    max_missing_tools: int | Unset = 5,
    include_foods_on_hand: bool | Unset = True,
    include_tools_on_hand: bool | Unset = True,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecipeSuggestionResponse]:
    """Suggest Recipes

    Args:
        group_slug (str):
        foods (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        limit (int | Unset):  Default: 10.
        max_missing_foods (int | Unset):  Default: 5.
        max_missing_tools (int | Unset):  Default: 5.
        include_foods_on_hand (bool | Unset):  Default: True.
        include_tools_on_hand (bool | Unset):  Default: True.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecipeSuggestionResponse]
    """

    kwargs = _get_kwargs(
        group_slug=group_slug,
        foods=foods,
        tools=tools,
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        limit=limit,
        max_missing_foods=max_missing_foods,
        max_missing_tools=max_missing_tools,
        include_foods_on_hand=include_foods_on_hand,
        include_tools_on_hand=include_tools_on_hand,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_slug: str,
    *,
    client: AuthenticatedClient | Client,
    foods: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    limit: int | Unset = 10,
    max_missing_foods: int | Unset = 5,
    max_missing_tools: int | Unset = 5,
    include_foods_on_hand: bool | Unset = True,
    include_tools_on_hand: bool | Unset = True,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | RecipeSuggestionResponse | None:
    """Suggest Recipes

    Args:
        group_slug (str):
        foods (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        limit (int | Unset):  Default: 10.
        max_missing_foods (int | Unset):  Default: 5.
        max_missing_tools (int | Unset):  Default: 5.
        include_foods_on_hand (bool | Unset):  Default: True.
        include_tools_on_hand (bool | Unset):  Default: True.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecipeSuggestionResponse
    """

    return sync_detailed(
        group_slug=group_slug,
        client=client,
        foods=foods,
        tools=tools,
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        limit=limit,
        max_missing_foods=max_missing_foods,
        max_missing_tools=max_missing_tools,
        include_foods_on_hand=include_foods_on_hand,
        include_tools_on_hand=include_tools_on_hand,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    group_slug: str,
    *,
    client: AuthenticatedClient | Client,
    foods: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    limit: int | Unset = 10,
    max_missing_foods: int | Unset = 5,
    max_missing_tools: int | Unset = 5,
    include_foods_on_hand: bool | Unset = True,
    include_tools_on_hand: bool | Unset = True,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | RecipeSuggestionResponse]:
    """Suggest Recipes

    Args:
        group_slug (str):
        foods (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        limit (int | Unset):  Default: 10.
        max_missing_foods (int | Unset):  Default: 5.
        max_missing_tools (int | Unset):  Default: 5.
        include_foods_on_hand (bool | Unset):  Default: True.
        include_tools_on_hand (bool | Unset):  Default: True.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | RecipeSuggestionResponse]
    """

    kwargs = _get_kwargs(
        group_slug=group_slug,
        foods=foods,
        tools=tools,
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        limit=limit,
        max_missing_foods=max_missing_foods,
        max_missing_tools=max_missing_tools,
        include_foods_on_hand=include_foods_on_hand,
        include_tools_on_hand=include_tools_on_hand,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_slug: str,
    *,
    client: AuthenticatedClient | Client,
    foods: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    limit: int | Unset = 10,
    max_missing_foods: int | Unset = 5,
    max_missing_tools: int | Unset = 5,
    include_foods_on_hand: bool | Unset = True,
    include_tools_on_hand: bool | Unset = True,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | RecipeSuggestionResponse | None:
    """Suggest Recipes

    Args:
        group_slug (str):
        foods (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        limit (int | Unset):  Default: 10.
        max_missing_foods (int | Unset):  Default: 5.
        max_missing_tools (int | Unset):  Default: 5.
        include_foods_on_hand (bool | Unset):  Default: True.
        include_tools_on_hand (bool | Unset):  Default: True.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | RecipeSuggestionResponse
    """

    return (
        await asyncio_detailed(
            group_slug=group_slug,
            client=client,
            foods=foods,
            tools=tools,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            limit=limit,
            max_missing_foods=max_missing_foods,
            max_missing_tools=max_missing_tools,
            include_foods_on_hand=include_foods_on_hand,
            include_tools_on_hand=include_tools_on_hand,
            accept_language=accept_language,
        )
    ).parsed
