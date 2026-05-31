from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.report_category import ReportCategory
from ..models.report_summary_status import ReportSummaryStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.report_entry_out import ReportEntryOut


T = TypeVar("T", bound="ReportOut")


@_attrs_define
class ReportOut:
    """
    Attributes:
        category (ReportCategory):
        group_id (str):
        name (str):
        id (str):
        timestamp (datetime.datetime | Unset):
        status (ReportSummaryStatus | Unset):
        entries (list[ReportEntryOut] | Unset):
    """

    category: ReportCategory
    group_id: str
    name: str
    id: str
    timestamp: datetime.datetime | Unset = UNSET
    status: ReportSummaryStatus | Unset = UNSET
    entries: list[ReportEntryOut] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        category = self.category.value

        group_id = self.group_id

        name = self.name

        id = self.id

        timestamp: str | Unset = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        entries: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.entries, Unset):
            entries = []
            for entries_item_data in self.entries:
                entries_item = entries_item_data.to_dict()
                entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "category": category,
                "groupId": group_id,
                "name": name,
                "id": id,
            }
        )
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if status is not UNSET:
            field_dict["status"] = status
        if entries is not UNSET:
            field_dict["entries"] = entries

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.report_entry_out import ReportEntryOut

        d = dict(src_dict)
        category = ReportCategory(d.pop("category"))

        group_id = d.pop("groupId")

        name = d.pop("name")

        id = d.pop("id")

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: datetime.datetime | Unset
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = datetime.datetime.fromisoformat(_timestamp)

        _status = d.pop("status", UNSET)
        status: ReportSummaryStatus | Unset
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ReportSummaryStatus(_status)

        _entries = d.pop("entries", UNSET)
        entries: list[ReportEntryOut] | Unset = UNSET
        if _entries is not UNSET:
            entries = []
            for entries_item_data in _entries:
                entries_item = ReportEntryOut.from_dict(entries_item_data)

                entries.append(entries_item)

        report_out = cls(
            category=category,
            group_id=group_id,
            name=name,
            id=id,
            timestamp=timestamp,
            status=status,
            entries=entries,
        )

        report_out.additional_properties = d
        return report_out

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
