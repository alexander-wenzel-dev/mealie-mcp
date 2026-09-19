from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ai_provider_create import AIProviderCreate
from ...models.ai_provider_test_result import AIProviderTestResult
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AIProviderCreate,
    accept_language: str | Unset | None = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/groups/ai-providers/providers/test",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AIProviderTestResult | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = AIProviderTestResult.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AIProviderTestResult | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AIProviderCreate,
    accept_language: str | Unset | None = UNSET,
) -> Response[AIProviderTestResult | HTTPValidationError]:
    """Test Ai Provider

     Test connectivity for a provider configuration before it has been saved.

    Args:
        accept_language (None | str | Unset):
        body (AIProviderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AIProviderTestResult | HTTPValidationError]
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
    body: AIProviderCreate,
    accept_language: str | Unset | None = UNSET,
) -> AIProviderTestResult | HTTPValidationError | None:
    """Test Ai Provider

     Test connectivity for a provider configuration before it has been saved.

    Args:
        accept_language (None | str | Unset):
        body (AIProviderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AIProviderTestResult | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AIProviderCreate,
    accept_language: str | Unset | None = UNSET,
) -> Response[AIProviderTestResult | HTTPValidationError]:
    """Test Ai Provider

     Test connectivity for a provider configuration before it has been saved.

    Args:
        accept_language (None | str | Unset):
        body (AIProviderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AIProviderTestResult | HTTPValidationError]
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
    body: AIProviderCreate,
    accept_language: str | Unset | None = UNSET,
) -> AIProviderTestResult | HTTPValidationError | None:
    """Test Ai Provider

     Test connectivity for a provider configuration before it has been saved.

    Args:
        accept_language (None | str | Unset):
        body (AIProviderCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AIProviderTestResult | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
