from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GroupDataExport")


@_attrs_define
class GroupDataExport:
    """
    Attributes:
        id (str):
        group_id (str):
        name (str):
        filename (str):
        path (str):
        size (str):
        expires (datetime.datetime):
    """

    id: str
    group_id: str
    name: str
    filename: str
    path: str
    size: str
    expires: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        group_id = self.group_id

        name = self.name

        filename = self.filename

        path = self.path

        size = self.size

        expires = self.expires.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "groupId": group_id,
                "name": name,
                "filename": filename,
                "path": path,
                "size": size,
                "expires": expires,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        group_id = d.pop("groupId")

        name = d.pop("name")

        filename = d.pop("filename")

        path = d.pop("path")

        size = d.pop("size")

        expires = datetime.datetime.fromisoformat(d.pop("expires"))

        group_data_export = cls(
            id=id,
            group_id=group_id,
            name=name,
            filename=filename,
            path=path,
            size=size,
            expires=expires,
        )

        group_data_export.additional_properties = d
        return group_data_export

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
