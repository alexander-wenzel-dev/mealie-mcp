from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateGroupPreferences")


@_attrs_define
class UpdateGroupPreferences:
    """
    Attributes:
        private_group (bool | Unset):  Default: True.
        show_announcements (bool | Unset):  Default: True.
    """

    private_group: bool | Unset = True
    show_announcements: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        private_group = self.private_group

        show_announcements = self.show_announcements

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if private_group is not UNSET:
            field_dict["privateGroup"] = private_group
        if show_announcements is not UNSET:
            field_dict["showAnnouncements"] = show_announcements

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        private_group = d.pop("privateGroup", UNSET)

        show_announcements = d.pop("showAnnouncements", UNSET)

        update_group_preferences = cls(
            private_group=private_group,
            show_announcements=show_announcements,
        )

        update_group_preferences.additional_properties = d
        return update_group_preferences

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
