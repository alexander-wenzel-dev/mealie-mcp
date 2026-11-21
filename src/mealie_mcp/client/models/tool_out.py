from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ToolOut")


@_attrs_define
class ToolOut:
    """
    Attributes:
        id (str):
        group_id (str):
        name (str):
        slug (str):
        recipe_count (int):  Default: 0.
        households_with_tool (list[str]):
    """

    id: str
    group_id: str
    name: str
    slug: str
    households_with_tool: list[str]
    recipe_count: int = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        group_id = self.group_id

        name = self.name

        slug = self.slug

        recipe_count = self.recipe_count

        households_with_tool = self.households_with_tool

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "groupId": group_id,
                "name": name,
                "slug": slug,
                "recipeCount": recipe_count,
                "householdsWithTool": households_with_tool,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        group_id = d.pop("groupId")

        name = d.pop("name")

        slug = d.pop("slug")

        recipe_count = d.pop("recipeCount")

        households_with_tool = cast(list[str], d.pop("householdsWithTool"))

        tool_out = cls(
            id=id,
            group_id=group_id,
            name=name,
            slug=slug,
            recipe_count=recipe_count,
            households_with_tool=households_with_tool,
        )

        tool_out.additional_properties = d
        return tool_out

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
