from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.order_by_null_position import OrderByNullPosition
from ...models.order_direction import OrderDirection
from ...models.pagination_base_recipe_summary import PaginationBaseRecipeSummary
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    categories: list[str] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    foods: list[str] | None | Unset = UNSET,
    households: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    cookbook: None | str | Unset = UNSET,
    require_all_categories: bool | Unset = False,
    require_all_tags: bool | Unset = False,
    require_all_tools: bool | Unset = False,
    require_all_foods: bool | Unset = False,
    search: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

    json_categories: list[str] | None | Unset
    if isinstance(categories, Unset):
        json_categories = UNSET
    elif isinstance(categories, list):
        json_categories = []
        for categories_type_0_item_data in categories:
            categories_type_0_item: str
            categories_type_0_item = categories_type_0_item_data
            json_categories.append(categories_type_0_item)

    else:
        json_categories = categories
    params["categories"] = json_categories

    json_tags: list[str] | None | Unset
    if isinstance(tags, Unset):
        json_tags = UNSET
    elif isinstance(tags, list):
        json_tags = []
        for tags_type_0_item_data in tags:
            tags_type_0_item: str
            tags_type_0_item = tags_type_0_item_data
            json_tags.append(tags_type_0_item)

    else:
        json_tags = tags
    params["tags"] = json_tags

    json_tools: list[str] | None | Unset
    if isinstance(tools, Unset):
        json_tools = UNSET
    elif isinstance(tools, list):
        json_tools = []
        for tools_type_0_item_data in tools:
            tools_type_0_item: str
            tools_type_0_item = tools_type_0_item_data
            json_tools.append(tools_type_0_item)

    else:
        json_tools = tools
    params["tools"] = json_tools

    json_foods: list[str] | None | Unset
    if isinstance(foods, Unset):
        json_foods = UNSET
    elif isinstance(foods, list):
        json_foods = []
        for foods_type_0_item_data in foods:
            foods_type_0_item: str
            foods_type_0_item = foods_type_0_item_data
            json_foods.append(foods_type_0_item)

    else:
        json_foods = foods
    params["foods"] = json_foods

    json_households: list[str] | None | Unset
    if isinstance(households, Unset):
        json_households = UNSET
    elif isinstance(households, list):
        json_households = []
        for households_type_0_item_data in households:
            households_type_0_item: str
            households_type_0_item = households_type_0_item_data
            json_households.append(households_type_0_item)

    else:
        json_households = households
    params["households"] = json_households

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

    params["page"] = page

    params["perPage"] = per_page

    json_cookbook: None | str | Unset
    if isinstance(cookbook, Unset):
        json_cookbook = UNSET
    else:
        json_cookbook = cookbook
    params["cookbook"] = json_cookbook

    params["requireAllCategories"] = require_all_categories

    params["requireAllTags"] = require_all_tags

    params["requireAllTools"] = require_all_tools

    params["requireAllFoods"] = require_all_foods

    json_search: None | str | Unset
    if isinstance(search, Unset):
        json_search = UNSET
    else:
        json_search = search
    params["search"] = json_search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/recipes",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PaginationBaseRecipeSummary | None:
    if response.status_code == 200:
        response_200 = PaginationBaseRecipeSummary.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | PaginationBaseRecipeSummary]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    categories: list[str] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    foods: list[str] | None | Unset = UNSET,
    households: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    cookbook: None | str | Unset = UNSET,
    require_all_categories: bool | Unset = False,
    require_all_tags: bool | Unset = False,
    require_all_tools: bool | Unset = False,
    require_all_foods: bool | Unset = False,
    search: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginationBaseRecipeSummary]:
    """Get All

    Args:
        categories (list[str] | None | Unset):
        tags (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        foods (list[str] | None | Unset):
        households (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        cookbook (None | str | Unset):
        require_all_categories (bool | Unset):  Default: False.
        require_all_tags (bool | Unset):  Default: False.
        require_all_tools (bool | Unset):  Default: False.
        require_all_foods (bool | Unset):  Default: False.
        search (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginationBaseRecipeSummary]
    """

    kwargs = _get_kwargs(
        categories=categories,
        tags=tags,
        tools=tools,
        foods=foods,
        households=households,
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        page=page,
        per_page=per_page,
        cookbook=cookbook,
        require_all_categories=require_all_categories,
        require_all_tags=require_all_tags,
        require_all_tools=require_all_tools,
        require_all_foods=require_all_foods,
        search=search,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    categories: list[str] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    foods: list[str] | None | Unset = UNSET,
    households: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    cookbook: None | str | Unset = UNSET,
    require_all_categories: bool | Unset = False,
    require_all_tags: bool | Unset = False,
    require_all_tools: bool | Unset = False,
    require_all_foods: bool | Unset = False,
    search: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginationBaseRecipeSummary | None:
    """Get All

    Args:
        categories (list[str] | None | Unset):
        tags (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        foods (list[str] | None | Unset):
        households (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        cookbook (None | str | Unset):
        require_all_categories (bool | Unset):  Default: False.
        require_all_tags (bool | Unset):  Default: False.
        require_all_tools (bool | Unset):  Default: False.
        require_all_foods (bool | Unset):  Default: False.
        search (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginationBaseRecipeSummary
    """

    return sync_detailed(
        client=client,
        categories=categories,
        tags=tags,
        tools=tools,
        foods=foods,
        households=households,
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        page=page,
        per_page=per_page,
        cookbook=cookbook,
        require_all_categories=require_all_categories,
        require_all_tags=require_all_tags,
        require_all_tools=require_all_tools,
        require_all_foods=require_all_foods,
        search=search,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    categories: list[str] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    foods: list[str] | None | Unset = UNSET,
    households: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    cookbook: None | str | Unset = UNSET,
    require_all_categories: bool | Unset = False,
    require_all_tags: bool | Unset = False,
    require_all_tools: bool | Unset = False,
    require_all_foods: bool | Unset = False,
    search: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PaginationBaseRecipeSummary]:
    """Get All

    Args:
        categories (list[str] | None | Unset):
        tags (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        foods (list[str] | None | Unset):
        households (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        cookbook (None | str | Unset):
        require_all_categories (bool | Unset):  Default: False.
        require_all_tags (bool | Unset):  Default: False.
        require_all_tools (bool | Unset):  Default: False.
        require_all_foods (bool | Unset):  Default: False.
        search (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PaginationBaseRecipeSummary]
    """

    kwargs = _get_kwargs(
        categories=categories,
        tags=tags,
        tools=tools,
        foods=foods,
        households=households,
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        page=page,
        per_page=per_page,
        cookbook=cookbook,
        require_all_categories=require_all_categories,
        require_all_tags=require_all_tags,
        require_all_tools=require_all_tools,
        require_all_foods=require_all_foods,
        search=search,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    categories: list[str] | None | Unset = UNSET,
    tags: list[str] | None | Unset = UNSET,
    tools: list[str] | None | Unset = UNSET,
    foods: list[str] | None | Unset = UNSET,
    households: list[str] | None | Unset = UNSET,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    cookbook: None | str | Unset = UNSET,
    require_all_categories: bool | Unset = False,
    require_all_tags: bool | Unset = False,
    require_all_tools: bool | Unset = False,
    require_all_foods: bool | Unset = False,
    search: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | PaginationBaseRecipeSummary | None:
    """Get All

    Args:
        categories (list[str] | None | Unset):
        tags (list[str] | None | Unset):
        tools (list[str] | None | Unset):
        foods (list[str] | None | Unset):
        households (list[str] | None | Unset):
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        cookbook (None | str | Unset):
        require_all_categories (bool | Unset):  Default: False.
        require_all_tags (bool | Unset):  Default: False.
        require_all_tools (bool | Unset):  Default: False.
        require_all_foods (bool | Unset):  Default: False.
        search (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PaginationBaseRecipeSummary
    """

    return (
        await asyncio_detailed(
            client=client,
            categories=categories,
            tags=tags,
            tools=tools,
            foods=foods,
            households=households,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            cookbook=cookbook,
            require_all_categories=require_all_categories,
            require_all_tags=require_all_tags,
            require_all_tools=require_all_tools,
            require_all_foods=require_all_foods,
            search=search,
            accept_language=accept_language,
        )
    ).parsed
