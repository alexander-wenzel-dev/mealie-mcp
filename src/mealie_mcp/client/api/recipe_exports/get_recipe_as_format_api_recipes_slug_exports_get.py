from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    slug: str,
    *,
    template_name: str,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

    params["template_name"] = template_name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/recipes/{slug}/exports".format(
            slug=quote(str(slug), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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
    slug: str,
    *,
    client: AuthenticatedClient,
    template_name: str,
    accept_language: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get Recipe As Format

     ## Parameters
    `template_name`: The name of the template to use to use in the exports listed. Template type will
    automatically
    be set on the backend. Because of this, it's important that your templates have unique names. See
    available
    names and formats in the /api/recipes/exports endpoint.

    Args:
        slug (str):
        template_name (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        slug=slug,
        template_name=template_name,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slug: str,
    *,
    client: AuthenticatedClient,
    template_name: str,
    accept_language: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Get Recipe As Format

     ## Parameters
    `template_name`: The name of the template to use to use in the exports listed. Template type will
    automatically
    be set on the backend. Because of this, it's important that your templates have unique names. See
    available
    names and formats in the /api/recipes/exports endpoint.

    Args:
        slug (str):
        template_name (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        slug=slug,
        client=client,
        template_name=template_name,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    slug: str,
    *,
    client: AuthenticatedClient,
    template_name: str,
    accept_language: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get Recipe As Format

     ## Parameters
    `template_name`: The name of the template to use to use in the exports listed. Template type will
    automatically
    be set on the backend. Because of this, it's important that your templates have unique names. See
    available
    names and formats in the /api/recipes/exports endpoint.

    Args:
        slug (str):
        template_name (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        slug=slug,
        template_name=template_name,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slug: str,
    *,
    client: AuthenticatedClient,
    template_name: str,
    accept_language: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Get Recipe As Format

     ## Parameters
    `template_name`: The name of the template to use to use in the exports listed. Template type will
    automatically
    be set on the backend. Because of this, it's important that your templates have unique names. See
    available
    names and formats in the /api/recipes/exports endpoint.

    Args:
        slug (str):
        template_name (str):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            slug=slug,
            client=client,
            template_name=template_name,
            accept_language=accept_language,
        )
    ).parsed
