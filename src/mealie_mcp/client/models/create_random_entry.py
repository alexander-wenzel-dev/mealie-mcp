from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_entry_type import PlanEntryType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateRandomEntry")


@_attrs_define
class CreateRandomEntry:
    """
    Attributes:
        date (datetime.date):
        entry_type (PlanEntryType | Unset):
    """

    date: datetime.date
    entry_type: PlanEntryType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        entry_type: str | Unset = UNSET
        if not isinstance(self.entry_type, Unset):
            entry_type = self.entry_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
            }
        )
        if entry_type is not UNSET:
            field_dict["entryType"] = entry_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))

        _entry_type = d.pop("entryType", UNSET)
        entry_type: PlanEntryType | Unset
        if isinstance(_entry_type, Unset):
            entry_type = UNSET
        else:
            entry_type = PlanEntryType(_entry_type)

        create_random_entry = cls(
            date=date,
            entry_type=entry_type,
        )

        create_random_entry.additional_properties = d
        return create_random_entry

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
