from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.group_recipe_action_type import GroupRecipeActionType

T = TypeVar("T", bound="SaveGroupRecipeAction")


@_attrs_define
class SaveGroupRecipeAction:
    """
    Attributes:
        action_type (GroupRecipeActionType):
        title (str):
        url (str):
        group_id (str):
        household_id (str):
    """

    action_type: GroupRecipeActionType
    title: str
    url: str
    group_id: str
    household_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action_type = self.action_type.value

        title = self.title

        url = self.url

        group_id = self.group_id

        household_id = self.household_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "actionType": action_type,
                "title": title,
                "url": url,
                "groupId": group_id,
                "householdId": household_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action_type = GroupRecipeActionType(d.pop("actionType"))

        title = d.pop("title")

        url = d.pop("url")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        save_group_recipe_action = cls(
            action_type=action_type,
            title=title,
            url=url,
            group_id=group_id,
            household_id=household_id,
        )

        save_group_recipe_action.additional_properties = d
        return save_group_recipe_action

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
