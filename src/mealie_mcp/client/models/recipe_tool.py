from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeTool")


@_attrs_define
class RecipeTool:
    """
    Attributes:
        id (str):
        name (str):
        slug (str):
        group_id (None | str | Unset):
        households_with_tool (list[str] | Unset):
    """

    id: str
    name: str
    slug: str
    group_id: None | str | Unset = UNSET
    households_with_tool: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        slug = self.slug

        group_id: None | str | Unset
        if isinstance(self.group_id, Unset):
            group_id = UNSET
        else:
            group_id = self.group_id

        households_with_tool: list[str] | Unset = UNSET
        if not isinstance(self.households_with_tool, Unset):
            households_with_tool = self.households_with_tool

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "slug": slug,
            }
        )
        if group_id is not UNSET:
            field_dict["groupId"] = group_id
        if households_with_tool is not UNSET:
            field_dict["householdsWithTool"] = households_with_tool

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        slug = d.pop("slug")

        def _parse_group_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_id = _parse_group_id(d.pop("groupId", UNSET))

        households_with_tool = cast(list[str], d.pop("householdsWithTool", UNSET))

        recipe_tool = cls(
            id=id,
            name=name,
            slug=slug,
            group_id=group_id,
            households_with_tool=households_with_tool,
        )

        recipe_tool.additional_properties = d
        return recipe_tool

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
