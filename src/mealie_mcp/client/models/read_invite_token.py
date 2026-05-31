from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ReadInviteToken")


@_attrs_define
class ReadInviteToken:
    """
    Attributes:
        token (str):
        uses_left (int):
        group_id (UUID):
        household_id (UUID):
    """

    token: str
    uses_left: int
    group_id: UUID
    household_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        uses_left = self.uses_left

        group_id = str(self.group_id)

        household_id = str(self.household_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "usesLeft": uses_left,
                "groupId": group_id,
                "householdId": household_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        uses_left = d.pop("usesLeft")

        group_id = UUID(d.pop("groupId"))

        household_id = UUID(d.pop("householdId"))

        read_invite_token = cls(
            token=token,
            uses_left=uses_left,
            group_id=group_id,
            household_id=household_id,
        )

        read_invite_token.additional_properties = d
        return read_invite_token

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
