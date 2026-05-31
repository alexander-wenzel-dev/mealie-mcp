from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppTheme")


@_attrs_define
class AppTheme:
    """
    Attributes:
        light_primary (str | Unset):  Default: '#E58325'.
        light_accent (str | Unset):  Default: '#007A99'.
        light_secondary (str | Unset):  Default: '#973542'.
        light_success (str | Unset):  Default: '#43A047'.
        light_info (str | Unset):  Default: '#1976D2'.
        light_warning (str | Unset):  Default: '#FF6D00'.
        light_error (str | Unset):  Default: '#EF5350'.
        dark_primary (str | Unset):  Default: '#E58325'.
        dark_accent (str | Unset):  Default: '#007A99'.
        dark_secondary (str | Unset):  Default: '#973542'.
        dark_success (str | Unset):  Default: '#43A047'.
        dark_info (str | Unset):  Default: '#1976D2'.
        dark_warning (str | Unset):  Default: '#FF6D00'.
        dark_error (str | Unset):  Default: '#EF5350'.
    """

    light_primary: str | Unset = "#E58325"
    light_accent: str | Unset = "#007A99"
    light_secondary: str | Unset = "#973542"
    light_success: str | Unset = "#43A047"
    light_info: str | Unset = "#1976D2"
    light_warning: str | Unset = "#FF6D00"
    light_error: str | Unset = "#EF5350"
    dark_primary: str | Unset = "#E58325"
    dark_accent: str | Unset = "#007A99"
    dark_secondary: str | Unset = "#973542"
    dark_success: str | Unset = "#43A047"
    dark_info: str | Unset = "#1976D2"
    dark_warning: str | Unset = "#FF6D00"
    dark_error: str | Unset = "#EF5350"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        light_primary = self.light_primary

        light_accent = self.light_accent

        light_secondary = self.light_secondary

        light_success = self.light_success

        light_info = self.light_info

        light_warning = self.light_warning

        light_error = self.light_error

        dark_primary = self.dark_primary

        dark_accent = self.dark_accent

        dark_secondary = self.dark_secondary

        dark_success = self.dark_success

        dark_info = self.dark_info

        dark_warning = self.dark_warning

        dark_error = self.dark_error

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if light_primary is not UNSET:
            field_dict["lightPrimary"] = light_primary
        if light_accent is not UNSET:
            field_dict["lightAccent"] = light_accent
        if light_secondary is not UNSET:
            field_dict["lightSecondary"] = light_secondary
        if light_success is not UNSET:
            field_dict["lightSuccess"] = light_success
        if light_info is not UNSET:
            field_dict["lightInfo"] = light_info
        if light_warning is not UNSET:
            field_dict["lightWarning"] = light_warning
        if light_error is not UNSET:
            field_dict["lightError"] = light_error
        if dark_primary is not UNSET:
            field_dict["darkPrimary"] = dark_primary
        if dark_accent is not UNSET:
            field_dict["darkAccent"] = dark_accent
        if dark_secondary is not UNSET:
            field_dict["darkSecondary"] = dark_secondary
        if dark_success is not UNSET:
            field_dict["darkSuccess"] = dark_success
        if dark_info is not UNSET:
            field_dict["darkInfo"] = dark_info
        if dark_warning is not UNSET:
            field_dict["darkWarning"] = dark_warning
        if dark_error is not UNSET:
            field_dict["darkError"] = dark_error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        light_primary = d.pop("lightPrimary", UNSET)

        light_accent = d.pop("lightAccent", UNSET)

        light_secondary = d.pop("lightSecondary", UNSET)

        light_success = d.pop("lightSuccess", UNSET)

        light_info = d.pop("lightInfo", UNSET)

        light_warning = d.pop("lightWarning", UNSET)

        light_error = d.pop("lightError", UNSET)

        dark_primary = d.pop("darkPrimary", UNSET)

        dark_accent = d.pop("darkAccent", UNSET)

        dark_secondary = d.pop("darkSecondary", UNSET)

        dark_success = d.pop("darkSuccess", UNSET)

        dark_info = d.pop("darkInfo", UNSET)

        dark_warning = d.pop("darkWarning", UNSET)

        dark_error = d.pop("darkError", UNSET)

        app_theme = cls(
            light_primary=light_primary,
            light_accent=light_accent,
            light_secondary=light_secondary,
            light_success=light_success,
            light_info=light_info,
            light_warning=light_warning,
            light_error=light_error,
            dark_primary=dark_primary,
            dark_accent=dark_accent,
            dark_secondary=dark_secondary,
            dark_success=dark_success,
            dark_info=dark_info,
            dark_warning=dark_warning,
            dark_error=dark_error,
        )

        app_theme.additional_properties = d
        return app_theme

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
