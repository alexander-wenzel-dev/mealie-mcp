from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MultiPurposeLabelSummaryOutput")


@_attrs_define
class MultiPurposeLabelSummaryOutput:
    """
    Attributes:
        name (str):
        color (str):  Default: '#959595'.
        group_id (str):
        id (str):
    """

    name: str
    group_id: str
    id: str
    color: str = "#959595"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        color = self.color

        group_id = self.group_id

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "color": color,
                "groupId": group_id,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        color = d.pop("color")

        group_id = d.pop("groupId")

        id = d.pop("id")

        multi_purpose_label_summary_output = cls(
            name=name,
            color=color,
            group_id=group_id,
            id=id,
        )

        multi_purpose_label_summary_output.additional_properties = d
        return multi_purpose_label_summary_output

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
