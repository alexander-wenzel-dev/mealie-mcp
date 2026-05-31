from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MaintenanceSummary")


@_attrs_define
class MaintenanceSummary:
    """
    Attributes:
        data_dir_size (str):
        cleanable_images (int):
        cleanable_dirs (int):
    """

    data_dir_size: str
    cleanable_images: int
    cleanable_dirs: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data_dir_size = self.data_dir_size

        cleanable_images = self.cleanable_images

        cleanable_dirs = self.cleanable_dirs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataDirSize": data_dir_size,
                "cleanableImages": cleanable_images,
                "cleanableDirs": cleanable_dirs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_dir_size = d.pop("dataDirSize")

        cleanable_images = d.pop("cleanableImages")

        cleanable_dirs = d.pop("cleanableDirs")

        maintenance_summary = cls(
            data_dir_size=data_dir_size,
            cleanable_images=cleanable_images,
            cleanable_dirs=cleanable_dirs,
        )

        maintenance_summary.additional_properties = d
        return maintenance_summary

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
