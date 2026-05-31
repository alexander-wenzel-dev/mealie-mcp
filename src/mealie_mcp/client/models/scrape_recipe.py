from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScrapeRecipe")


@_attrs_define
class ScrapeRecipe:
    """
    Example:
        {'includeCategories': True, 'includeTags': True, 'url': 'https://myfavoriterecipes.com/recipes'}

    Attributes:
        url (str):
        include_tags (bool | Unset):  Default: False.
        include_categories (bool | Unset):  Default: False.
    """

    url: str
    include_tags: bool | Unset = False
    include_categories: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        include_tags = self.include_tags

        include_categories = self.include_categories

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if include_tags is not UNSET:
            field_dict["includeTags"] = include_tags
        if include_categories is not UNSET:
            field_dict["includeCategories"] = include_categories

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        include_tags = d.pop("includeTags", UNSET)

        include_categories = d.pop("includeCategories", UNSET)

        scrape_recipe = cls(
            url=url,
            include_tags=include_tags,
            include_categories=include_categories,
        )

        scrape_recipe.additional_properties = d
        return scrape_recipe

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
