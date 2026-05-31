from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.forgot_password import ForgotPassword
from ...models.http_validation_error import HTTPValidationError
from ...models.password_reset_token import PasswordResetToken
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ForgotPassword,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/admin/users/password-reset-token",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | PasswordResetToken | None:
    if response.status_code == 201:
        response_201 = PasswordResetToken.from_dict(response.json())

        return response_201

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | PasswordResetToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ForgotPassword,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PasswordResetToken]:
    """Generate Token

     Generates a reset token and returns it. This is an authenticated endpoint

    Args:
        accept_language (None | str | Unset):
        body (ForgotPassword):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PasswordResetToken]
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
    body: ForgotPassword,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | PasswordResetToken | None:
    """Generate Token

     Generates a reset token and returns it. This is an authenticated endpoint

    Args:
        accept_language (None | str | Unset):
        body (ForgotPassword):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PasswordResetToken
    """

    return sync_detailed(
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ForgotPassword,
    accept_language: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | PasswordResetToken]:
    """Generate Token

     Generates a reset token and returns it. This is an authenticated endpoint

    Args:
        accept_language (None | str | Unset):
        body (ForgotPassword):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | PasswordResetToken]
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
    body: ForgotPassword,
    accept_language: None | str | Unset = UNSET,
) -> HTTPValidationError | PasswordResetToken | None:
    """Generate Token

     Generates a reset token and returns it. This is an authenticated endpoint

    Args:
        accept_language (None | str | Unset):
        body (ForgotPassword):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | PasswordResetToken
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
