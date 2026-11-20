from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_draft import CategoryDraft
    from ..models.tag_draft import TagDraft


T = TypeVar("T", bound="RecipeUrlCreate")


@_attrs_define
class RecipeUrlCreate:
    """
    Attributes:
        url (str):
        categories (list[CategoryDraft] | None | Unset):
        tags (list[TagDraft] | None | Unset):
    """

    url: str
    categories: list[CategoryDraft] | Unset | None = UNSET
    tags: list[TagDraft] | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        categories: list[dict[str, Any]] | Unset | None
        if isinstance(self.categories, Unset):
            categories = UNSET
        elif isinstance(self.categories, list):
            categories = []
            for categories_type_0_item_data in self.categories:
                categories_type_0_item = categories_type_0_item_data.to_dict()
                categories.append(categories_type_0_item)

        else:
            categories = self.categories

        tags: list[dict[str, Any]] | Unset | None
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = []
            for tags_type_0_item_data in self.tags:
                tags_type_0_item = tags_type_0_item_data.to_dict()
                tags.append(tags_type_0_item)

        else:
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if categories is not UNSET:
            field_dict["categories"] = categories
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_draft import CategoryDraft  # noqa: PLC0415
        from ..models.tag_draft import TagDraft  # noqa: PLC0415

        d = dict(src_dict)
        url = d.pop("url")

        def _parse_categories(data: object) -> list[CategoryDraft] | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                categories_type_0 = []
                _categories_type_0 = data
                for categories_type_0_item_data in _categories_type_0:
                    categories_type_0_item = CategoryDraft.from_dict(categories_type_0_item_data)

                    categories_type_0.append(categories_type_0_item)

                return categories_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[CategoryDraft] | None | Unset, data)

        categories = _parse_categories(d.pop("categories", UNSET))

        def _parse_tags(data: object) -> list[TagDraft] | Unset | None:
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
                    tags_type_0_item = TagDraft.from_dict(tags_type_0_item_data)

                    tags_type_0.append(tags_type_0_item)

                return tags_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[TagDraft] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        recipe_url_create = cls(
            url=url,
            categories=categories,
            tags=tags,
        )

        recipe_url_create.additional_properties = d
        return recipe_url_create

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
