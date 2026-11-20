from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.category_out import CategoryOut
    from ..models.tag_out import TagOut
    from ..models.tool_out import ToolOut


T = TypeVar("T", bound="RecipeSummary")


@_attrs_define
class RecipeSummary:
    """A saved recipe without its ingredients, instructions and other details, as list views show it.

    Every recipe has an owner: list queries skip rows whose user (and so household) is gone.

        Attributes:
            id (str):
            user_id (str):
            household_id (str):
            group_id (str):
            name (str):
            slug (str):
            image (None | str):
            recipe_servings (float):  Default: 0.0.
            recipe_yield_quantity (float):  Default: 0.0.
            recipe_yield (None | str):
            total_time (None | str):
            prep_time (None | str):
            perform_time (None | str):
            total_time_seconds (int | None):
            prep_time_seconds (int | None):
            perform_time_seconds (int | None):
            description (None | str):  Default: ''.
            recipe_category (list[CategoryOut]):
            tags (list[TagOut]):
            tools (list[ToolOut]):
            rating (float | None):
            org_url (None | str):
            date_added (datetime.date | None):
            date_updated (datetime.datetime | None):
            created_at (datetime.datetime | None):
            updated_at (datetime.datetime | None):
    """

    id: str
    user_id: str
    household_id: str
    group_id: str
    name: str
    slug: str
    image: str | None
    recipe_yield: str | None
    total_time: str | None
    prep_time: str | None
    perform_time: str | None
    total_time_seconds: int | None
    prep_time_seconds: int | None
    perform_time_seconds: int | None
    recipe_category: list[CategoryOut]
    tags: list[TagOut]
    tools: list[ToolOut]
    rating: float | None
    org_url: str | None
    date_added: datetime.date | None
    date_updated: datetime.datetime | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    recipe_servings: float = 0.0
    recipe_yield_quantity: float = 0.0
    description: str | None = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        household_id = self.household_id

        group_id = self.group_id

        name = self.name

        slug = self.slug

        image: str | None
        image = self.image

        recipe_servings = self.recipe_servings

        recipe_yield_quantity = self.recipe_yield_quantity

        recipe_yield: str | None
        recipe_yield = self.recipe_yield

        total_time: str | None
        total_time = self.total_time

        prep_time: str | None
        prep_time = self.prep_time

        perform_time: str | None
        perform_time = self.perform_time

        total_time_seconds: int | None
        total_time_seconds = self.total_time_seconds

        prep_time_seconds: int | None
        prep_time_seconds = self.prep_time_seconds

        perform_time_seconds: int | None
        perform_time_seconds = self.perform_time_seconds

        description: str | None
        description = self.description

        recipe_category = []
        for recipe_category_item_data in self.recipe_category:
            recipe_category_item = recipe_category_item_data.to_dict()
            recipe_category.append(recipe_category_item)

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()
            tools.append(tools_item)

        rating: float | None
        rating = self.rating

        org_url: str | None
        org_url = self.org_url

        date_added: str | None
        if isinstance(self.date_added, datetime.date):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        date_updated: str | None
        if isinstance(self.date_updated, datetime.datetime):
            date_updated = self.date_updated.isoformat()
        else:
            date_updated = self.date_updated

        created_at: str | None
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: str | None
        if isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "userId": user_id,
                "householdId": household_id,
                "groupId": group_id,
                "name": name,
                "slug": slug,
                "image": image,
                "recipeServings": recipe_servings,
                "recipeYieldQuantity": recipe_yield_quantity,
                "recipeYield": recipe_yield,
                "totalTime": total_time,
                "prepTime": prep_time,
                "performTime": perform_time,
                "totalTimeSeconds": total_time_seconds,
                "prepTimeSeconds": prep_time_seconds,
                "performTimeSeconds": perform_time_seconds,
                "description": description,
                "recipeCategory": recipe_category,
                "tags": tags,
                "tools": tools,
                "rating": rating,
                "orgURL": org_url,
                "dateAdded": date_added,
                "dateUpdated": date_updated,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_out import CategoryOut  # noqa: PLC0415
        from ..models.tag_out import TagOut  # noqa: PLC0415
        from ..models.tool_out import ToolOut  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("userId")

        household_id = d.pop("householdId")

        group_id = d.pop("groupId")

        name = d.pop("name")

        slug = d.pop("slug")

        def _parse_image(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        image = _parse_image(d.pop("image"))

        recipe_servings = d.pop("recipeServings")

        recipe_yield_quantity = d.pop("recipeYieldQuantity")

        def _parse_recipe_yield(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        recipe_yield = _parse_recipe_yield(d.pop("recipeYield"))

        def _parse_total_time(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        total_time = _parse_total_time(d.pop("totalTime"))

        def _parse_prep_time(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        prep_time = _parse_prep_time(d.pop("prepTime"))

        def _parse_perform_time(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        perform_time = _parse_perform_time(d.pop("performTime"))

        def _parse_total_time_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        total_time_seconds = _parse_total_time_seconds(d.pop("totalTimeSeconds"))

        def _parse_prep_time_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        prep_time_seconds = _parse_prep_time_seconds(d.pop("prepTimeSeconds"))

        def _parse_perform_time_seconds(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        perform_time_seconds = _parse_perform_time_seconds(d.pop("performTimeSeconds"))

        def _parse_description(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        description = _parse_description(d.pop("description"))

        recipe_category = []
        _recipe_category = d.pop("recipeCategory")
        for recipe_category_item_data in _recipe_category:
            recipe_category_item = CategoryOut.from_dict(recipe_category_item_data)

            recipe_category.append(recipe_category_item)

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = TagOut.from_dict(tags_item_data)

            tags.append(tags_item)

        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = ToolOut.from_dict(tools_item_data)

            tools.append(tools_item)

        def _parse_rating(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rating = _parse_rating(d.pop("rating"))

        def _parse_org_url(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        org_url = _parse_org_url(d.pop("orgURL"))

        def _parse_date_added(data: object) -> datetime.date | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_added_type_0 = datetime.date.fromisoformat(data)

                return date_added_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.date | None, data)

        date_added = _parse_date_added(d.pop("dateAdded"))

        def _parse_date_updated(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_updated_type_0 = datetime.datetime.fromisoformat(data)

                return date_updated_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None, data)

        date_updated = _parse_date_updated(d.pop("dateUpdated"))

        def _parse_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None, data)

        created_at = _parse_created_at(d.pop("createdAt"))

        def _parse_updated_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None, data)

        updated_at = _parse_updated_at(d.pop("updatedAt"))

        recipe_summary = cls(
            id=id,
            user_id=user_id,
            household_id=household_id,
            group_id=group_id,
            name=name,
            slug=slug,
            image=image,
            recipe_servings=recipe_servings,
            recipe_yield_quantity=recipe_yield_quantity,
            recipe_yield=recipe_yield,
            total_time=total_time,
            prep_time=prep_time,
            perform_time=perform_time,
            total_time_seconds=total_time_seconds,
            prep_time_seconds=prep_time_seconds,
            perform_time_seconds=perform_time_seconds,
            description=description,
            recipe_category=recipe_category,
            tags=tags,
            tools=tools,
            rating=rating,
            org_url=org_url,
            date_added=date_added,
            date_updated=date_updated,
            created_at=created_at,
            updated_at=updated_at,
        )

        recipe_summary.additional_properties = d
        return recipe_summary

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
