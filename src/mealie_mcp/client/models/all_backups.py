from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.backup_file import BackupFile


T = TypeVar("T", bound="AllBackups")


@_attrs_define
class AllBackups:
    """
    Attributes:
        imports (list[BackupFile]):
        templates (list[str]):
    """

    imports: list[BackupFile]
    templates: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        imports = []
        for imports_item_data in self.imports:
            imports_item = imports_item_data.to_dict()
            imports.append(imports_item)

        templates = self.templates

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imports": imports,
                "templates": templates,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.backup_file import BackupFile

        d = dict(src_dict)
        imports = []
        _imports = d.pop("imports")
        for imports_item_data in _imports:
            imports_item = BackupFile.from_dict(imports_item_data)

            imports.append(imports_item)

        templates = cast(list[str], d.pop("templates"))

        all_backups = cls(
            imports=imports,
            templates=templates,
        )

        all_backups.additional_properties = d
        return all_backups

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
