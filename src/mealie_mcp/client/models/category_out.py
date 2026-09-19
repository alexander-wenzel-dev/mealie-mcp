from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CategoryOut")


@_attrs_define
class CategoryOut:
    """
    Attributes:
        name (str):
        id (str):
        group_id (str):
        slug (str):
        recipe_count (int | Unset):  Default: 0.
    """

    name: str
    id: str
    group_id: str
    slug: str
    recipe_count: int | Unset = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        id = self.id

        group_id = self.group_id

        slug = self.slug

        recipe_count = self.recipe_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "id": id,
                "groupId": group_id,
                "slug": slug,
            }
        )
        if recipe_count is not UNSET:
            field_dict["recipeCount"] = recipe_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        id = d.pop("id")

        group_id = d.pop("groupId")

        slug = d.pop("slug")

        recipe_count = d.pop("recipeCount", UNSET)

        category_out = cls(
            name=name,
            id=id,
            group_id=group_id,
            slug=slug,
            recipe_count=recipe_count,
        )

        category_out.additional_properties = d
        return category_out

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
