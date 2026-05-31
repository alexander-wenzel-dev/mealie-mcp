from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AppStartupInfo")


@_attrs_define
class AppStartupInfo:
    """
    Attributes:
        is_first_login (bool):
        is_demo (bool):
    """

    is_first_login: bool
    is_demo: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_first_login = self.is_first_login

        is_demo = self.is_demo

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "isFirstLogin": is_first_login,
                "isDemo": is_demo,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_first_login = d.pop("isFirstLogin")

        is_demo = d.pop("isDemo")

        app_startup_info = cls(
            is_first_login=is_first_login,
            is_demo=is_demo,
        )

        app_startup_info.additional_properties = d
        return app_startup_info

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
