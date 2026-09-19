from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ai_provider_test_result import AIProviderTestResult
from ...models.ai_provider_update import AIProviderUpdate
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    provider_id: str,
    *,
    body: AIProviderUpdate | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/groups/ai-providers/providers/{provider_id}/test".format(
            provider_id=quote(str(provider_id), safe=""),
        ),
    }

    if isinstance(body, AIProviderUpdate):
        _kwargs["json"] = body.to_dict()
    else:
        _kwargs["json"] = body

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
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: AIProviderUpdate | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> Response[AIProviderTestResult | HTTPValidationError]:
    """Test Saved Ai Provider

     Test connectivity for an already-saved provider.

    Accepts optional unsaved edits to test against instead of what's in the database - e.g.
    while editing a provider, the caller may have changed the model/base_url but left the API
    key blank (meaning "keep the existing one"), so a plain "unsaved" test can't be used since
    it has no way to supply that key. An `overrides.apiKey` of "" is treated the same way: keep
    the saved key rather than testing with an empty one.

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (AIProviderUpdate | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AIProviderTestResult | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        provider_id=provider_id,
        body=body,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: AIProviderUpdate | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> AIProviderTestResult | HTTPValidationError | None:
    """Test Saved Ai Provider

     Test connectivity for an already-saved provider.

    Accepts optional unsaved edits to test against instead of what's in the database - e.g.
    while editing a provider, the caller may have changed the model/base_url but left the API
    key blank (meaning "keep the existing one"), so a plain "unsaved" test can't be used since
    it has no way to supply that key. An `overrides.apiKey` of "" is treated the same way: keep
    the saved key rather than testing with an empty one.

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (AIProviderUpdate | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AIProviderTestResult | HTTPValidationError
    """

    return sync_detailed(
        provider_id=provider_id,
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: AIProviderUpdate | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> Response[AIProviderTestResult | HTTPValidationError]:
    """Test Saved Ai Provider

     Test connectivity for an already-saved provider.

    Accepts optional unsaved edits to test against instead of what's in the database - e.g.
    while editing a provider, the caller may have changed the model/base_url but left the API
    key blank (meaning "keep the existing one"), so a plain "unsaved" test can't be used since
    it has no way to supply that key. An `overrides.apiKey` of "" is treated the same way: keep
    the saved key rather than testing with an empty one.

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (AIProviderUpdate | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AIProviderTestResult | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        provider_id=provider_id,
        body=body,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    provider_id: str,
    *,
    client: AuthenticatedClient,
    body: AIProviderUpdate | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> AIProviderTestResult | HTTPValidationError | None:
    """Test Saved Ai Provider

     Test connectivity for an already-saved provider.

    Accepts optional unsaved edits to test against instead of what's in the database - e.g.
    while editing a provider, the caller may have changed the model/base_url but left the API
    key blank (meaning "keep the existing one"), so a plain "unsaved" test can't be used since
    it has no way to supply that key. An `overrides.apiKey` of "" is treated the same way: keep
    the saved key rather than testing with an empty one.

    Args:
        provider_id (str):
        accept_language (None | str | Unset):
        body (AIProviderUpdate | None | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AIProviderTestResult | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            provider_id=provider_id,
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
