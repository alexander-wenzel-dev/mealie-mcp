from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.report_category import ReportCategory
from ..models.report_summary_status import ReportSummaryStatus

if TYPE_CHECKING:
    from ..models.report_entry_out import ReportEntryOut


T = TypeVar("T", bound="ReportOut")


@_attrs_define
class ReportOut:
    """
    Attributes:
        timestamp (datetime.datetime):
        category (ReportCategory):
        group_id (str):
        name (str):
        status (ReportSummaryStatus):
        id (str):
        entries (list[ReportEntryOut]):
    """

    timestamp: datetime.datetime
    category: ReportCategory
    group_id: str
    name: str
    status: ReportSummaryStatus
    id: str
    entries: list[ReportEntryOut]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        category = self.category.value

        group_id = self.group_id

        name = self.name

        status = self.status.value

        id = self.id

        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()
            entries.append(entries_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "category": category,
                "groupId": group_id,
                "name": name,
                "status": status,
                "id": id,
                "entries": entries,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.report_entry_out import ReportEntryOut  # noqa: PLC0415

        d = dict(src_dict)
        timestamp = datetime.datetime.fromisoformat(d.pop("timestamp"))

        category = ReportCategory(d.pop("category"))

        group_id = d.pop("groupId")

        name = d.pop("name")

        status = ReportSummaryStatus(d.pop("status"))

        id = d.pop("id")

        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = ReportEntryOut.from_dict(entries_item_data)

            entries.append(entries_item)

        report_out = cls(
            timestamp=timestamp,
            category=category,
            group_id=group_id,
            name=name,
            status=status,
            id=id,
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
