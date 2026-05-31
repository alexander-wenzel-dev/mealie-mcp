from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AppStatistics")


@_attrs_define
class AppStatistics:
    """
    Attributes:
        total_recipes (int):
        total_users (int):
        total_households (int):
        total_groups (int):
        uncategorized_recipes (int):
        untagged_recipes (int):
    """

    total_recipes: int
    total_users: int
    total_households: int
    total_groups: int
    uncategorized_recipes: int
    untagged_recipes: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_recipes = self.total_recipes

        total_users = self.total_users

        total_households = self.total_households

        total_groups = self.total_groups

        uncategorized_recipes = self.uncategorized_recipes

        untagged_recipes = self.untagged_recipes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "totalRecipes": total_recipes,
                "totalUsers": total_users,
                "totalHouseholds": total_households,
                "totalGroups": total_groups,
                "uncategorizedRecipes": uncategorized_recipes,
                "untaggedRecipes": untagged_recipes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total_recipes = d.pop("totalRecipes")

        total_users = d.pop("totalUsers")

        total_households = d.pop("totalHouseholds")

        total_groups = d.pop("totalGroups")

        uncategorized_recipes = d.pop("uncategorizedRecipes")

        untagged_recipes = d.pop("untaggedRecipes")

        app_statistics = cls(
            total_recipes=total_recipes,
            total_users=total_users,
            total_households=total_households,
            total_groups=total_groups,
            uncategorized_recipes=uncategorized_recipes,
            untagged_recipes=untagged_recipes,
        )

        app_statistics.additional_properties = d
        return app_statistics

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
