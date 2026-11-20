from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ai_prompt_override_update import AIPromptOverrideUpdate
from ...models.ai_prompts_out import AIPromptsOut
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_id: str,
    prompt_name: str,
    *,
    body: AIPromptOverrideUpdate,
    accept_language: str | Unset | None = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/admin/groups/{group_id}/ai-providers/prompts/{prompt_name}".format(
            group_id=quote(str(group_id), safe=""),
            prompt_name=quote(str(prompt_name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AIPromptsOut | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = AIPromptsOut.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AIPromptsOut | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str,
    prompt_name: str,
    *,
    client: AuthenticatedClient,
    body: AIPromptOverrideUpdate,
    accept_language: str | Unset | None = UNSET,
) -> Response[AIPromptsOut | HTTPValidationError]:
    """Update Ai Prompt

     Append to or override a prompt. The group-wide instructions (`global`) can only be appended.

    Args:
        group_id (str):
        prompt_name (str):
        accept_language (None | str | Unset):
        body (AIPromptOverrideUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AIPromptsOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        prompt_name=prompt_name,
        body=body,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    prompt_name: str,
    *,
    client: AuthenticatedClient,
    body: AIPromptOverrideUpdate,
    accept_language: str | Unset | None = UNSET,
) -> AIPromptsOut | HTTPValidationError | None:
    """Update Ai Prompt

     Append to or override a prompt. The group-wide instructions (`global`) can only be appended.

    Args:
        group_id (str):
        prompt_name (str):
        accept_language (None | str | Unset):
        body (AIPromptOverrideUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AIPromptsOut | HTTPValidationError
    """

    return sync_detailed(
        group_id=group_id,
        prompt_name=prompt_name,
        client=client,
        body=body,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    prompt_name: str,
    *,
    client: AuthenticatedClient,
    body: AIPromptOverrideUpdate,
    accept_language: str | Unset | None = UNSET,
) -> Response[AIPromptsOut | HTTPValidationError]:
    """Update Ai Prompt

     Append to or override a prompt. The group-wide instructions (`global`) can only be appended.

    Args:
        group_id (str):
        prompt_name (str):
        accept_language (None | str | Unset):
        body (AIPromptOverrideUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AIPromptsOut | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        prompt_name=prompt_name,
        body=body,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    prompt_name: str,
    *,
    client: AuthenticatedClient,
    body: AIPromptOverrideUpdate,
    accept_language: str | Unset | None = UNSET,
) -> AIPromptsOut | HTTPValidationError | None:
    """Update Ai Prompt

     Append to or override a prompt. The group-wide instructions (`global`) can only be appended.

    Args:
        group_id (str):
        prompt_name (str):
        accept_language (None | str | Unset):
        body (AIPromptOverrideUpdate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AIPromptsOut | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            prompt_name=prompt_name,
            client=client,
            body=body,
            accept_language=accept_language,
        )
    ).parsed
