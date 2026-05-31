from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.group_event_notifier_options_out import GroupEventNotifierOptionsOut


T = TypeVar("T", bound="GroupEventNotifierOut")


@_attrs_define
class GroupEventNotifierOut:
    """
    Attributes:
        id (str):
        name (str):
        enabled (bool):
        group_id (str):
        household_id (str):
        options (GroupEventNotifierOptionsOut):
    """

    id: str
    name: str
    enabled: bool
    group_id: str
    household_id: str
    options: GroupEventNotifierOptionsOut
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        enabled = self.enabled

        group_id = self.group_id

        household_id = self.household_id

        options = self.options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "enabled": enabled,
                "groupId": group_id,
                "householdId": household_id,
                "options": options,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.group_event_notifier_options_out import GroupEventNotifierOptionsOut

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        enabled = d.pop("enabled")

        group_id = d.pop("groupId")

        household_id = d.pop("householdId")

        options = GroupEventNotifierOptionsOut.from_dict(d.pop("options"))

        group_event_notifier_out = cls(
            id=id,
            name=name,
            enabled=enabled,
            group_id=group_id,
            household_id=household_id,
            options=options,
        )

        group_event_notifier_out.additional_properties = d
        return group_event_notifier_out

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
