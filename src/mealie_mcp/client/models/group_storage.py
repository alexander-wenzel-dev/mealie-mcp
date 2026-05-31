from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GroupStorage")


@_attrs_define
class GroupStorage:
    """
    Attributes:
        used_storage_bytes (int):
        used_storage_str (str):
        total_storage_bytes (int):
        total_storage_str (str):
    """

    used_storage_bytes: int
    used_storage_str: str
    total_storage_bytes: int
    total_storage_str: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        used_storage_bytes = self.used_storage_bytes

        used_storage_str = self.used_storage_str

        total_storage_bytes = self.total_storage_bytes

        total_storage_str = self.total_storage_str

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "usedStorageBytes": used_storage_bytes,
                "usedStorageStr": used_storage_str,
                "totalStorageBytes": total_storage_bytes,
                "totalStorageStr": total_storage_str,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        used_storage_bytes = d.pop("usedStorageBytes")

        used_storage_str = d.pop("usedStorageStr")

        total_storage_bytes = d.pop("totalStorageBytes")

        total_storage_str = d.pop("totalStorageStr")

        group_storage = cls(
            used_storage_bytes=used_storage_bytes,
            used_storage_str=used_storage_str,
            total_storage_bytes=total_storage_bytes,
            total_storage_str=total_storage_str,
        )

        group_storage.additional_properties = d
        return group_storage

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
