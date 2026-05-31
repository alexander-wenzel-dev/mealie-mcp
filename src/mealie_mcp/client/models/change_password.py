from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangePassword")


@_attrs_define
class ChangePassword:
    """
    Attributes:
        new_password (str):
        current_password (str | Unset):  Default: ''.
    """

    new_password: str
    current_password: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_password = self.new_password

        current_password = self.current_password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "newPassword": new_password,
            }
        )
        if current_password is not UNSET:
            field_dict["currentPassword"] = current_password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        new_password = d.pop("newPassword")

        current_password = d.pop("currentPassword", UNSET)

        change_password = cls(
            new_password=new_password,
            current_password=current_password,
        )

        change_password.additional_properties = d
        return change_password

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
