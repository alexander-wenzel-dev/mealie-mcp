from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.tag_base import TagBase


T = TypeVar("T", bound="AssignTags")


@_attrs_define
class AssignTags:
    """
    Attributes:
        recipes (list[str]):
        tags (list[TagBase]):
    """

    recipes: list[str]
    tags: list[TagBase]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipes = self.recipes

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipes": recipes,
                "tags": tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tag_base import TagBase

        d = dict(src_dict)
        recipes = cast(list[str], d.pop("recipes"))

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = TagBase.from_dict(tags_item_data)

            tags.append(tags_item)

        assign_tags = cls(
            recipes=recipes,
            tags=tags,
        )

        assign_tags.additional_properties = d
        return assign_tags

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
