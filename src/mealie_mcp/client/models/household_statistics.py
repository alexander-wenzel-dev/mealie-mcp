from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="HouseholdStatistics")


@_attrs_define
class HouseholdStatistics:
    """
    Attributes:
        total_recipes (int):
        total_users (int):
        total_categories (int):
        total_tags (int):
        total_tools (int):
    """

    total_recipes: int
    total_users: int
    total_categories: int
    total_tags: int
    total_tools: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_recipes = self.total_recipes

        total_users = self.total_users

        total_categories = self.total_categories

        total_tags = self.total_tags

        total_tools = self.total_tools

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "totalRecipes": total_recipes,
                "totalUsers": total_users,
                "totalCategories": total_categories,
                "totalTags": total_tags,
                "totalTools": total_tools,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_recipes = d.pop("totalRecipes")

        total_users = d.pop("totalUsers")

        total_categories = d.pop("totalCategories")

        total_tags = d.pop("totalTags")

        total_tools = d.pop("totalTools")

        household_statistics = cls(
            total_recipes=total_recipes,
            total_users=total_users,
            total_categories=total_categories,
            total_tags=total_tags,
            total_tools=total_tools,
        )

        household_statistics.additional_properties = d
        return household_statistics

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
