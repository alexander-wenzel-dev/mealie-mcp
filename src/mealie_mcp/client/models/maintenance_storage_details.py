from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MaintenanceStorageDetails")


@_attrs_define
class MaintenanceStorageDetails:
    """
    Attributes:
        temp_dir_size (str):
        backups_dir_size (str):
        groups_dir_size (str):
        recipes_dir_size (str):
        user_dir_size (str):
    """

    temp_dir_size: str
    backups_dir_size: str
    groups_dir_size: str
    recipes_dir_size: str
    user_dir_size: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        temp_dir_size = self.temp_dir_size

        backups_dir_size = self.backups_dir_size

        groups_dir_size = self.groups_dir_size

        recipes_dir_size = self.recipes_dir_size

        user_dir_size = self.user_dir_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tempDirSize": temp_dir_size,
                "backupsDirSize": backups_dir_size,
                "groupsDirSize": groups_dir_size,
                "recipesDirSize": recipes_dir_size,
                "userDirSize": user_dir_size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        temp_dir_size = d.pop("tempDirSize")

        backups_dir_size = d.pop("backupsDirSize")

        groups_dir_size = d.pop("groupsDirSize")

        recipes_dir_size = d.pop("recipesDirSize")

        user_dir_size = d.pop("userDirSize")

        maintenance_storage_details = cls(
            temp_dir_size=temp_dir_size,
            backups_dir_size=backups_dir_size,
            groups_dir_size=groups_dir_size,
            recipes_dir_size=recipes_dir_size,
            user_dir_size=user_dir_size,
        )

        maintenance_storage_details.additional_properties = d
        return maintenance_storage_details

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
