from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LongLiveTokenIn")


@_attrs_define
class LongLiveTokenIn:
    """
    Attributes:
        name (str):
        integration_id (str | Unset):  Default: 'generic'.
    """

    name: str
    integration_id: str | Unset = "generic"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        integration_id = self.integration_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if integration_id is not UNSET:
            field_dict["integrationId"] = integration_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        integration_id = d.pop("integrationId", UNSET)

        long_live_token_in = cls(
            name=name,
            integration_id=integration_id,
        )

        long_live_token_in.additional_properties = d
        return long_live_token_in

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
