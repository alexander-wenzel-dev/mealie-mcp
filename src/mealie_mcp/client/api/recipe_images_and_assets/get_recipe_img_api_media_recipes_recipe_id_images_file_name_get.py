from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.image_type import ImageType
from ...types import Response


def _get_kwargs(
    recipe_id: str,
    file_name: ImageType,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/media/recipes/{recipe_id}/images/{file_name}".format(
            recipe_id=quote(str(recipe_id), safe=""),
            file_name=quote(str(file_name), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recipe_id: str,
    file_name: ImageType,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    """Get Recipe Img

     Takes in a recipe id, returns the static image. This route is proxied in the docker image
    and should not hit the API in production

    Args:
        recipe_id (str):
        file_name (ImageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        recipe_id=recipe_id,
        file_name=file_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recipe_id: str,
    file_name: ImageType,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    """Get Recipe Img

     Takes in a recipe id, returns the static image. This route is proxied in the docker image
    and should not hit the API in production

    Args:
        recipe_id (str):
        file_name (ImageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        recipe_id=recipe_id,
        file_name=file_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    recipe_id: str,
    file_name: ImageType,
    *,
    client: AuthenticatedClient | Client,
) -> Response[Any | HTTPValidationError]:
    """Get Recipe Img

     Takes in a recipe id, returns the static image. This route is proxied in the docker image
    and should not hit the API in production

    Args:
        recipe_id (str):
        file_name (ImageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        recipe_id=recipe_id,
        file_name=file_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recipe_id: str,
    file_name: ImageType,
    *,
    client: AuthenticatedClient | Client,
) -> Any | HTTPValidationError | None:
    """Get Recipe Img

     Takes in a recipe id, returns the static image. This route is proxied in the docker image
    and should not hit the API in production

    Args:
        recipe_id (str):
        file_name (ImageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            recipe_id=recipe_id,
            file_name=file_name,
            client=client,
        )
    ).parsed
