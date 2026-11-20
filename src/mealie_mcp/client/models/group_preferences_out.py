from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GroupPreferencesOut")


@_attrs_define
class GroupPreferencesOut:
    """
    Attributes:
        private_group (bool):  Default: True.
        show_announcements (bool):  Default: True.
        group_id (UUID):
        id (str):
    """

    group_id: UUID
    id: str
    private_group: bool = True
    show_announcements: bool = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        private_group = self.private_group

        show_announcements = self.show_announcements

        group_id = str(self.group_id)

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "privateGroup": private_group,
                "showAnnouncements": show_announcements,
                "groupId": group_id,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        private_group = d.pop("privateGroup")

        show_announcements = d.pop("showAnnouncements")

        group_id = UUID(d.pop("groupId"))

        id = d.pop("id")

        group_preferences_out = cls(
            private_group=private_group,
            show_announcements=show_announcements,
            group_id=group_id,
            id=id,
        )

        group_preferences_out.additional_properties = d
        return group_preferences_out

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
