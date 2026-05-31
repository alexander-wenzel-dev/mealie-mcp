from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_category import RecipeCategory
    from ..models.recipe_tag import RecipeTag
    from ..models.recipe_tool import RecipeTool


T = TypeVar("T", bound="RecipeSummary")


@_attrs_define
class RecipeSummary:
    """
    Attributes:
        id (None | str | Unset):
        user_id (str | Unset):
        household_id (str | Unset):
        group_id (str | Unset):
        name (None | str | Unset):
        slug (str | Unset):  Default: ''.
        image (Any | None | Unset):
        recipe_servings (float | Unset):  Default: 0.0.
        recipe_yield_quantity (float | Unset):  Default: 0.0.
        recipe_yield (None | str | Unset):
        total_time (None | str | Unset):
        prep_time (None | str | Unset):
        cook_time (None | str | Unset):
        perform_time (None | str | Unset):
        description (None | str | Unset):  Default: ''.
        recipe_category (list[RecipeCategory] | None | Unset):
        tags (list[RecipeTag] | None | Unset):
        tools (list[RecipeTool] | Unset):
        rating (float | None | Unset):
        org_url (None | str | Unset):
        date_added (datetime.date | None | Unset):
        date_updated (datetime.datetime | None | Unset):
        created_at (datetime.datetime | None | Unset):
        updated_at (datetime.datetime | None | Unset):
        last_made (datetime.datetime | None | Unset):
    """

    id: None | str | Unset = UNSET
    user_id: str | Unset = UNSET
    household_id: str | Unset = UNSET
    group_id: str | Unset = UNSET
    name: None | str | Unset = UNSET
    slug: str | Unset = ""
    image: Any | None | Unset = UNSET
    recipe_servings: float | Unset = 0.0
    recipe_yield_quantity: float | Unset = 0.0
    recipe_yield: None | str | Unset = UNSET
    total_time: None | str | Unset = UNSET
    prep_time: None | str | Unset = UNSET
    cook_time: None | str | Unset = UNSET
    perform_time: None | str | Unset = UNSET
    description: None | str | Unset = ""
    recipe_category: list[RecipeCategory] | None | Unset = UNSET
    tags: list[RecipeTag] | None | Unset = UNSET
    tools: list[RecipeTool] | Unset = UNSET
    rating: float | None | Unset = UNSET
    org_url: None | str | Unset = UNSET
    date_added: datetime.date | None | Unset = UNSET
    date_updated: datetime.datetime | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    last_made: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        user_id = self.user_id

        household_id = self.household_id

        group_id = self.group_id

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        slug = self.slug

        image: Any | None | Unset
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        recipe_servings = self.recipe_servings

        recipe_yield_quantity = self.recipe_yield_quantity

        recipe_yield: None | str | Unset
        if isinstance(self.recipe_yield, Unset):
            recipe_yield = UNSET
        else:
            recipe_yield = self.recipe_yield

        total_time: None | str | Unset
        if isinstance(self.total_time, Unset):
            total_time = UNSET
        else:
            total_time = self.total_time

        prep_time: None | str | Unset
        if isinstance(self.prep_time, Unset):
            prep_time = UNSET
        else:
            prep_time = self.prep_time

        cook_time: None | str | Unset
        if isinstance(self.cook_time, Unset):
            cook_time = UNSET
        else:
            cook_time = self.cook_time

        perform_time: None | str | Unset
        if isinstance(self.perform_time, Unset):
            perform_time = UNSET
        else:
            perform_time = self.perform_time

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        recipe_category: list[dict[str, Any]] | None | Unset
        if isinstance(self.recipe_category, Unset):
            recipe_category = UNSET
        elif isinstance(self.recipe_category, list):
            recipe_category = []
            for recipe_category_type_0_item_data in self.recipe_category:
                recipe_category_type_0_item = recipe_category_type_0_item_data.to_dict()
                recipe_category.append(recipe_category_type_0_item)

        else:
            recipe_category = self.recipe_category

        tags: list[dict[str, Any]] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = []
            for tags_type_0_item_data in self.tags:
                tags_type_0_item = tags_type_0_item_data.to_dict()
                tags.append(tags_type_0_item)

        else:
            tags = self.tags

        tools: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.tools, Unset):
            tools = []
            for tools_item_data in self.tools:
                tools_item = tools_item_data.to_dict()
                tools.append(tools_item)

        rating: float | None | Unset
        if isinstance(self.rating, Unset):
            rating = UNSET
        else:
            rating = self.rating

        org_url: None | str | Unset
        if isinstance(self.org_url, Unset):
            org_url = UNSET
        else:
            org_url = self.org_url

        date_added: None | str | Unset
        if isinstance(self.date_added, Unset):
            date_added = UNSET
        elif isinstance(self.date_added, datetime.date):
            date_added = self.date_added.isoformat()
        else:
            date_added = self.date_added

        date_updated: None | str | Unset
        if isinstance(self.date_updated, Unset):
            date_updated = UNSET
        elif isinstance(self.date_updated, datetime.datetime):
            date_updated = self.date_updated.isoformat()
        else:
            date_updated = self.date_updated

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        last_made: None | str | Unset
        if isinstance(self.last_made, Unset):
            last_made = UNSET
        elif isinstance(self.last_made, datetime.datetime):
            last_made = self.last_made.isoformat()
        else:
            last_made = self.last_made

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if household_id is not UNSET:
            field_dict["householdId"] = household_id
        if group_id is not UNSET:
            field_dict["groupId"] = group_id
        if name is not UNSET:
            field_dict["name"] = name
        if slug is not UNSET:
            field_dict["slug"] = slug
        if image is not UNSET:
            field_dict["image"] = image
        if recipe_servings is not UNSET:
            field_dict["recipeServings"] = recipe_servings
        if recipe_yield_quantity is not UNSET:
            field_dict["recipeYieldQuantity"] = recipe_yield_quantity
        if recipe_yield is not UNSET:
            field_dict["recipeYield"] = recipe_yield
        if total_time is not UNSET:
            field_dict["totalTime"] = total_time
        if prep_time is not UNSET:
            field_dict["prepTime"] = prep_time
        if cook_time is not UNSET:
            field_dict["cookTime"] = cook_time
        if perform_time is not UNSET:
            field_dict["performTime"] = perform_time
        if description is not UNSET:
            field_dict["description"] = description
        if recipe_category is not UNSET:
            field_dict["recipeCategory"] = recipe_category
        if tags is not UNSET:
            field_dict["tags"] = tags
        if tools is not UNSET:
            field_dict["tools"] = tools
        if rating is not UNSET:
            field_dict["rating"] = rating
        if org_url is not UNSET:
            field_dict["orgURL"] = org_url
        if date_added is not UNSET:
            field_dict["dateAdded"] = date_added
        if date_updated is not UNSET:
            field_dict["dateUpdated"] = date_updated
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if last_made is not UNSET:
            field_dict["lastMade"] = last_made

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_category import RecipeCategory
        from ..models.recipe_tag import RecipeTag
        from ..models.recipe_tool import RecipeTool

        d = dict(src_dict)

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        user_id = d.pop("userId", UNSET)

        household_id = d.pop("householdId", UNSET)

        group_id = d.pop("groupId", UNSET)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        slug = d.pop("slug", UNSET)

        def _parse_image(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        image = _parse_image(d.pop("image", UNSET))

        recipe_servings = d.pop("recipeServings", UNSET)

        recipe_yield_quantity = d.pop("recipeYieldQuantity", UNSET)

        def _parse_recipe_yield(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        recipe_yield = _parse_recipe_yield(d.pop("recipeYield", UNSET))

        def _parse_total_time(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        total_time = _parse_total_time(d.pop("totalTime", UNSET))

        def _parse_prep_time(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prep_time = _parse_prep_time(d.pop("prepTime", UNSET))

        def _parse_cook_time(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        cook_time = _parse_cook_time(d.pop("cookTime", UNSET))

        def _parse_perform_time(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        perform_time = _parse_perform_time(d.pop("performTime", UNSET))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_recipe_category(data: object) -> list[RecipeCategory] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                recipe_category_type_0 = []
                _recipe_category_type_0 = data
                for recipe_category_type_0_item_data in _recipe_category_type_0:
                    recipe_category_type_0_item = RecipeCategory.from_dict(
                        recipe_category_type_0_item_data
                    )

                    recipe_category_type_0.append(recipe_category_type_0_item)

                return recipe_category_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[RecipeCategory] | None | Unset, data)

        recipe_category = _parse_recipe_category(d.pop("recipeCategory", UNSET))

        def _parse_tags(data: object) -> list[RecipeTag] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = []
                _tags_type_0 = data
                for tags_type_0_item_data in _tags_type_0:
                    tags_type_0_item = RecipeTag.from_dict(tags_type_0_item_data)

                    tags_type_0.append(tags_type_0_item)

                return tags_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[RecipeTag] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        _tools = d.pop("tools", UNSET)
        tools: list[RecipeTool] | Unset = UNSET
        if _tools is not UNSET:
            tools = []
            for tools_item_data in _tools:
                tools_item = RecipeTool.from_dict(tools_item_data)

                tools.append(tools_item)

        def _parse_rating(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        rating = _parse_rating(d.pop("rating", UNSET))

        def _parse_org_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        org_url = _parse_org_url(d.pop("orgURL", UNSET))

        def _parse_date_added(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_added_type_0 = datetime.date.fromisoformat(data)

                return date_added_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.date | None | Unset, data)

        date_added = _parse_date_added(d.pop("dateAdded", UNSET))

        def _parse_date_updated(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_updated_type_0 = datetime.datetime.fromisoformat(data)

                return date_updated_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        date_updated = _parse_date_updated(d.pop("dateUpdated", UNSET))

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = datetime.datetime.fromisoformat(data)

                return created_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = datetime.datetime.fromisoformat(data)

                return updated_at_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updatedAt", UNSET))

        def _parse_last_made(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_made_type_0 = datetime.datetime.fromisoformat(data)

                return last_made_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_made = _parse_last_made(d.pop("lastMade", UNSET))

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
            cook_time=cook_time,
            perform_time=perform_time,
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
            last_made=last_made,
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
