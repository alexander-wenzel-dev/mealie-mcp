from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.plan_entry_type import PlanEntryType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    token: str,
    *,
    types: list[PlanEntryType] | Unset | None = UNSET,
    include_notes: bool | Unset = True,
    tz: str | Unset | None = UNSET,
    lang: str | Unset | None = UNSET,
    duration: int | Unset = 60,
    summary: str | Unset = "${type}: ${title}",
    description: str | Unset = "${note}\n\n${url}",
    breakfast: str | Unset | None = UNSET,
    lunch: str | Unset | None = UNSET,
    dinner: str | Unset | None = UNSET,
    side: str | Unset | None = UNSET,
    snack: str | Unset | None = UNSET,
    drink: str | Unset | None = UNSET,
    dessert: str | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(accept_language, Unset):
        headers["accept-language"] = accept_language

    params: dict[str, Any] = {}

    json_types: list[str] | Unset | None
    if isinstance(types, Unset):
        json_types = UNSET
    elif isinstance(types, list):
        json_types = []
        for types_type_0_item_data in types:
            types_type_0_item = types_type_0_item_data.value
            json_types.append(types_type_0_item)

    else:
        json_types = types
    params["types"] = json_types

    params["includeNotes"] = include_notes

    json_tz: str | Unset | None
    if isinstance(tz, Unset):
        json_tz = UNSET
    else:
        json_tz = tz
    params["tz"] = json_tz

    json_lang: str | Unset | None
    if isinstance(lang, Unset):
        json_lang = UNSET
    else:
        json_lang = lang
    params["lang"] = json_lang

    params["duration"] = duration

    params["summary"] = summary

    params["description"] = description

    json_breakfast: str | Unset | None
    if isinstance(breakfast, Unset):
        json_breakfast = UNSET
    else:
        json_breakfast = breakfast
    params["breakfast"] = json_breakfast

    json_lunch: str | Unset | None
    if isinstance(lunch, Unset):
        json_lunch = UNSET
    else:
        json_lunch = lunch
    params["lunch"] = json_lunch

    json_dinner: str | Unset | None
    if isinstance(dinner, Unset):
        json_dinner = UNSET
    else:
        json_dinner = dinner
    params["dinner"] = json_dinner

    json_side: str | Unset | None
    if isinstance(side, Unset):
        json_side = UNSET
    else:
        json_side = side
    params["side"] = json_side

    json_snack: str | Unset | None
    if isinstance(snack, Unset):
        json_snack = UNSET
    else:
        json_snack = snack
    params["snack"] = json_snack

    json_drink: str | Unset | None
    if isinstance(drink, Unset):
        json_drink = UNSET
    else:
        json_drink = drink
    params["drink"] = json_drink

    json_dessert: str | Unset | None
    if isinstance(dessert, Unset):
        json_dessert = UNSET
    else:
        json_dessert = dessert
    params["dessert"] = json_dessert

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/households/mealplans/ical/{token}".format(
            token=quote(str(token), safe=""),
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
    token: str,
    *,
    client: AuthenticatedClient | Client,
    types: list[PlanEntryType] | Unset | None = UNSET,
    include_notes: bool | Unset = True,
    tz: str | Unset | None = UNSET,
    lang: str | Unset | None = UNSET,
    duration: int | Unset = 60,
    summary: str | Unset = "${type}: ${title}",
    description: str | Unset = "${note}\n\n${url}",
    breakfast: str | Unset | None = UNSET,
    lunch: str | Unset | None = UNSET,
    dinner: str | Unset | None = UNSET,
    side: str | Unset | None = UNSET,
    snack: str | Unset | None = UNSET,
    drink: str | Unset | None = UNSET,
    dessert: str | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get Mealplan Ical Feed

     Public iCal feed of the household's meal plan. No authentication is required;
    access is controlled by the secret token in the URL.

    Args:
        token (str):
        types (list[PlanEntryType] | None | Unset):
        include_notes (bool | Unset):  Default: True.
        tz (None | str | Unset):
        lang (None | str | Unset):
        duration (int | Unset):  Default: 60.
        summary (str | Unset):  Default: '${type}: ${title}'.
        description (str | Unset):  Default: '${note}\\n\\n${url}'.
        breakfast (None | str | Unset):
        lunch (None | str | Unset):
        dinner (None | str | Unset):
        side (None | str | Unset):
        snack (None | str | Unset):
        drink (None | str | Unset):
        dessert (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        token=token,
        types=types,
        include_notes=include_notes,
        tz=tz,
        lang=lang,
        duration=duration,
        summary=summary,
        description=description,
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        side=side,
        snack=snack,
        drink=drink,
        dessert=dessert,
        accept_language=accept_language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token: str,
    *,
    client: AuthenticatedClient | Client,
    types: list[PlanEntryType] | Unset | None = UNSET,
    include_notes: bool | Unset = True,
    tz: str | Unset | None = UNSET,
    lang: str | Unset | None = UNSET,
    duration: int | Unset = 60,
    summary: str | Unset = "${type}: ${title}",
    description: str | Unset = "${note}\n\n${url}",
    breakfast: str | Unset | None = UNSET,
    lunch: str | Unset | None = UNSET,
    dinner: str | Unset | None = UNSET,
    side: str | Unset | None = UNSET,
    snack: str | Unset | None = UNSET,
    drink: str | Unset | None = UNSET,
    dessert: str | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> Any | HTTPValidationError | None:
    """Get Mealplan Ical Feed

     Public iCal feed of the household's meal plan. No authentication is required;
    access is controlled by the secret token in the URL.

    Args:
        token (str):
        types (list[PlanEntryType] | None | Unset):
        include_notes (bool | Unset):  Default: True.
        tz (None | str | Unset):
        lang (None | str | Unset):
        duration (int | Unset):  Default: 60.
        summary (str | Unset):  Default: '${type}: ${title}'.
        description (str | Unset):  Default: '${note}\\n\\n${url}'.
        breakfast (None | str | Unset):
        lunch (None | str | Unset):
        dinner (None | str | Unset):
        side (None | str | Unset):
        snack (None | str | Unset):
        drink (None | str | Unset):
        dessert (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        token=token,
        client=client,
        types=types,
        include_notes=include_notes,
        tz=tz,
        lang=lang,
        duration=duration,
        summary=summary,
        description=description,
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        side=side,
        snack=snack,
        drink=drink,
        dessert=dessert,
        accept_language=accept_language,
    ).parsed


async def asyncio_detailed(
    token: str,
    *,
    client: AuthenticatedClient | Client,
    types: list[PlanEntryType] | Unset | None = UNSET,
    include_notes: bool | Unset = True,
    tz: str | Unset | None = UNSET,
    lang: str | Unset | None = UNSET,
    duration: int | Unset = 60,
    summary: str | Unset = "${type}: ${title}",
    description: str | Unset = "${note}\n\n${url}",
    breakfast: str | Unset | None = UNSET,
    lunch: str | Unset | None = UNSET,
    dinner: str | Unset | None = UNSET,
    side: str | Unset | None = UNSET,
    snack: str | Unset | None = UNSET,
    drink: str | Unset | None = UNSET,
    dessert: str | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> Response[Any | HTTPValidationError]:
    """Get Mealplan Ical Feed

     Public iCal feed of the household's meal plan. No authentication is required;
    access is controlled by the secret token in the URL.

    Args:
        token (str):
        types (list[PlanEntryType] | None | Unset):
        include_notes (bool | Unset):  Default: True.
        tz (None | str | Unset):
        lang (None | str | Unset):
        duration (int | Unset):  Default: 60.
        summary (str | Unset):  Default: '${type}: ${title}'.
        description (str | Unset):  Default: '${note}\\n\\n${url}'.
        breakfast (None | str | Unset):
        lunch (None | str | Unset):
        dinner (None | str | Unset):
        side (None | str | Unset):
        snack (None | str | Unset):
        drink (None | str | Unset):
        dessert (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        token=token,
        types=types,
        include_notes=include_notes,
        tz=tz,
        lang=lang,
        duration=duration,
        summary=summary,
        description=description,
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        side=side,
        snack=snack,
        drink=drink,
        dessert=dessert,
        accept_language=accept_language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token: str,
    *,
    client: AuthenticatedClient | Client,
    types: list[PlanEntryType] | Unset | None = UNSET,
    include_notes: bool | Unset = True,
    tz: str | Unset | None = UNSET,
    lang: str | Unset | None = UNSET,
    duration: int | Unset = 60,
    summary: str | Unset = "${type}: ${title}",
    description: str | Unset = "${note}\n\n${url}",
    breakfast: str | Unset | None = UNSET,
    lunch: str | Unset | None = UNSET,
    dinner: str | Unset | None = UNSET,
    side: str | Unset | None = UNSET,
    snack: str | Unset | None = UNSET,
    drink: str | Unset | None = UNSET,
    dessert: str | Unset | None = UNSET,
    accept_language: str | Unset | None = UNSET,
) -> Any | HTTPValidationError | None:
    """Get Mealplan Ical Feed

     Public iCal feed of the household's meal plan. No authentication is required;
    access is controlled by the secret token in the URL.

    Args:
        token (str):
        types (list[PlanEntryType] | None | Unset):
        include_notes (bool | Unset):  Default: True.
        tz (None | str | Unset):
        lang (None | str | Unset):
        duration (int | Unset):  Default: 60.
        summary (str | Unset):  Default: '${type}: ${title}'.
        description (str | Unset):  Default: '${note}\\n\\n${url}'.
        breakfast (None | str | Unset):
        lunch (None | str | Unset):
        dinner (None | str | Unset):
        side (None | str | Unset):
        snack (None | str | Unset):
        drink (None | str | Unset):
        dessert (None | str | Unset):
        accept_language (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            token=token,
            client=client,
            types=types,
            include_notes=include_notes,
            tz=tz,
            lang=lang,
            duration=duration,
            summary=summary,
            description=description,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            side=side,
            snack=snack,
            drink=drink,
            dessert=dessert,
            accept_language=accept_language,
        )
    ).parsed
