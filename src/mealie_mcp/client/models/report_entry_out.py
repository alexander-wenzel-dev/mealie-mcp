from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ReportEntryOut")


@_attrs_define
class ReportEntryOut:
    """
    Attributes:
        report_id (str):
        message (str):
        id (str):
        timestamp (datetime.datetime | Unset):
        success (bool | Unset):  Default: True.
        exception (str | Unset):  Default: ''.
    """

    report_id: str
    message: str
    id: str
    timestamp: datetime.datetime | Unset = UNSET
    success: bool | Unset = True
    exception: str | Unset = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        report_id = self.report_id

        message = self.message

        id = self.id

        timestamp: str | Unset = UNSET
        if not isinstance(self.timestamp, Unset):
            timestamp = self.timestamp.isoformat()

        success = self.success

        exception = self.exception

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reportId": report_id,
                "message": message,
                "id": id,
            }
        )
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp
        if success is not UNSET:
            field_dict["success"] = success
        if exception is not UNSET:
            field_dict["exception"] = exception

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        report_id = d.pop("reportId")

        message = d.pop("message")

        id = d.pop("id")

        _timestamp = d.pop("timestamp", UNSET)
        timestamp: datetime.datetime | Unset
        if isinstance(_timestamp, Unset):
            timestamp = UNSET
        else:
            timestamp = datetime.datetime.fromisoformat(_timestamp)

        success = d.pop("success", UNSET)

        exception = d.pop("exception", UNSET)

        report_entry_out = cls(
            report_id=report_id,
            message=message,
            id=id,
            timestamp=timestamp,
            success=success,
            exception=exception,
        )

        report_entry_out.additional_properties = d
        return report_entry_out

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
