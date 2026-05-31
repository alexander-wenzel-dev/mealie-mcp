from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_create_recipe_from_image_api_recipes_create_image_post import (
    BodyCreateRecipeFromImageApiRecipesCreateImagePost,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodyCreateRecipeFromImageApiRecipesCreateImagePost,
    translate_language: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

    json_translate_language: None | str | Unset
    if isinstance(translate_language, Unset):
        json_translate_language = UNSET
    else:
        json_translate_language = translate_language
    params["translateLanguage"] = json_translate_language

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/recipes/create/image",
        "params": params,
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 201:
        response_201 = response.json()
        return response_201

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
    *,
    client: AuthenticatedClient,
    body: BodyCreateRecipeFromImageApiRecipesCreateImagePost,
    translate_language: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Create Recipe From Image

     Create a recipe from an image using OpenAI.
    Optionally specify a language for it to translate the recipe to.

    Args:
        translate_language (None | str | Unset):
        accept_language (None | str | Unset):
        body (BodyCreateRecipeFromImageApiRecipesCreateImagePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        translate_language=translate_language,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: BodyCreateRecipeFromImageApiRecipesCreateImagePost,
    translate_language: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Create Recipe From Image

     Create a recipe from an image using OpenAI.
    Optionally specify a language for it to translate the recipe to.

    Args:
        translate_language (None | str | Unset):
        accept_language (None | str | Unset):
        body (BodyCreateRecipeFromImageApiRecipesCreateImagePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        translate_language=translate_language,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyCreateRecipeFromImageApiRecipesCreateImagePost,
    translate_language: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Create Recipe From Image

     Create a recipe from an image using OpenAI.
    Optionally specify a language for it to translate the recipe to.

    Args:
        translate_language (None | str | Unset):
        accept_language (None | str | Unset):
        body (BodyCreateRecipeFromImageApiRecipesCreateImagePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        translate_language=translate_language,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BodyCreateRecipeFromImageApiRecipesCreateImagePost,
    translate_language: None | str | Unset = UNSET,
    accept_language: None | str | Unset = UNSET,
) -> Any | HTTPValidationError | None:
    """Create Recipe From Image

     Create a recipe from an image using OpenAI.
    Optionally specify a language for it to translate the recipe to.

    Args:
        translate_language (None | str | Unset):
        accept_language (None | str | Unset):
        body (BodyCreateRecipeFromImageApiRecipesCreateImagePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            translate_language=translate_language,
            accept_language=accept_language,
        )
    ).parsed
