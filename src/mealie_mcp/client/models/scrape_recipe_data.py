from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ScrapeRecipeData")


@_attrs_define
class ScrapeRecipeData:
    """
    Attributes:
        data (str):
        include_tags (bool | Unset):  Default: False.
        include_categories (bool | Unset):  Default: False.
        url (None | str | Unset):
    """

    data: str
    include_tags: bool | Unset = False
    include_categories: bool | Unset = False
    url: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data

        include_tags = self.include_tags

        include_categories = self.include_categories

        url: None | str | Unset
        if isinstance(self.url, Unset):
            url = UNSET
        else:
            url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )
        if include_tags is not UNSET:
            field_dict["includeTags"] = include_tags
        if include_categories is not UNSET:
            field_dict["includeCategories"] = include_categories
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data = d.pop("data")

        include_tags = d.pop("includeTags", UNSET)

        include_categories = d.pop("includeCategories", UNSET)

        def _parse_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        url = _parse_url(d.pop("url", UNSET))

        scrape_recipe_data = cls(
            data=data,
            include_tags=include_tags,
            include_categories=include_categories,
            url=url,
        )

        scrape_recipe_data.additional_properties = d
        return scrape_recipe_data

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
