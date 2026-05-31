from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReadGroupPreferences")


@_attrs_define
class ReadGroupPreferences:
    """
    Attributes:
        group_id (UUID):
        id (str):
        private_group (bool | Unset):  Default: True.
        show_announcements (bool | Unset):  Default: True.
    """

    group_id: UUID
    id: str
    private_group: bool | Unset = True
    show_announcements: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_id = str(self.group_id)

        id = self.id

        private_group = self.private_group

        show_announcements = self.show_announcements

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "groupId": group_id,
                "id": id,
            }
        )
        if private_group is not UNSET:
            field_dict["privateGroup"] = private_group
        if show_announcements is not UNSET:
            field_dict["showAnnouncements"] = show_announcements

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_id = UUID(d.pop("groupId"))

        id = d.pop("id")

        private_group = d.pop("privateGroup", UNSET)

        show_announcements = d.pop("showAnnouncements", UNSET)

        read_group_preferences = cls(
            group_id=group_id,
            id=id,
            private_group=private_group,
            show_announcements=show_announcements,
        )

        read_group_preferences.additional_properties = d
        return read_group_preferences

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
