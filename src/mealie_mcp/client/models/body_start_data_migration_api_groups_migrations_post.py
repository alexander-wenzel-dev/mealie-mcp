from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..models.supported_migrations import SupportedMigrations
from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyStartDataMigrationApiGroupsMigrationsPost")


@_attrs_define
class BodyStartDataMigrationApiGroupsMigrationsPost:
    """
    Attributes:
        migration_type (SupportedMigrations):
        archive (str):
        add_migration_tag (bool | Unset):  Default: False.
    """

    migration_type: SupportedMigrations
    archive: str
    add_migration_tag: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        migration_type = self.migration_type.value

        archive = self.archive

        add_migration_tag = self.add_migration_tag

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "migration_type": migration_type,
                "archive": archive,
            }
        )
        if add_migration_tag is not UNSET:
            field_dict["add_migration_tag"] = add_migration_tag

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(
            ("migration_type", (None, str(self.migration_type.value).encode(), "text/plain"))
        )

        files.append(("archive", (None, str(self.archive).encode(), "text/plain")))

        if not isinstance(self.add_migration_tag, Unset):
            files.append(
                ("add_migration_tag", (None, str(self.add_migration_tag).encode(), "text/plain"))
            )

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        migration_type = SupportedMigrations(d.pop("migration_type"))

        archive = d.pop("archive")

        add_migration_tag = d.pop("add_migration_tag", UNSET)

        body_start_data_migration_api_groups_migrations_post = cls(
            migration_type=migration_type,
            archive=archive,
            add_migration_tag=add_migration_tag,
        )

        body_start_data_migration_api_groups_migrations_post.additional_properties = d
        return body_start_data_migration_api_groups_migrations_post

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
