from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.order_by_null_position import OrderByNullPosition
from ...models.order_direction import OrderDirection
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

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

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/households/shopping/lists",
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | None:
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError]:
    """Get All

    Args:
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        page=page,
        per_page=per_page,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | None:
    """Get All

    Args:
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return sync_detailed(
        client=client,
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        page=page,
        per_page=per_page,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError]:
    """Get All

    Args:
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        order_by=order_by,
        order_by_null_position=order_by_null_position,
        order_direction=order_direction,
        query_filter=query_filter,
        pagination_seed=pagination_seed,
        page=page,
        per_page=per_page,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    order_by: None | str | Unset = UNSET,
    order_by_null_position: None | OrderByNullPosition | Unset = UNSET,
    order_direction: OrderDirection | Unset = UNSET,
    query_filter: None | str | Unset = UNSET,
    pagination_seed: None | str | Unset = UNSET,
    page: int | Unset = 1,
    per_page: int | Unset = 50,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | None:
    """Get All

    Args:
        order_by (None | str | Unset):
        order_by_null_position (None | OrderByNullPosition | Unset):
        order_direction (OrderDirection | Unset):
        query_filter (None | str | Unset):
        pagination_seed (None | str | Unset):
        page (int | Unset):  Default: 1.
        per_page (int | Unset):  Default: 50.
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            order_by=order_by,
            order_by_null_position=order_by_null_position,
            order_direction=order_direction,
            query_filter=query_filter,
            pagination_seed=pagination_seed,
            page=page,
            per_page=per_page,
            accept_language=accept_language,
        )
    ).parsed
