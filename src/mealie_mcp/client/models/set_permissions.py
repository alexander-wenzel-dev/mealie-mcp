from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetPermissions")


@_attrs_define
class SetPermissions:
    """
    Attributes:
        user_id (str):
        can_manage_household (bool | Unset):  Default: False.
        can_manage (bool | Unset):  Default: False.
        can_invite (bool | Unset):  Default: False.
        can_organize (bool | Unset):  Default: False.
    """

    user_id: str
    can_manage_household: bool | Unset = False
    can_manage: bool | Unset = False
    can_invite: bool | Unset = False
    can_organize: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        can_manage_household = self.can_manage_household

        can_manage = self.can_manage

        can_invite = self.can_invite

        can_organize = self.can_organize

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "userId": user_id,
            }
        )
        if can_manage_household is not UNSET:
            field_dict["canManageHousehold"] = can_manage_household
        if can_manage is not UNSET:
            field_dict["canManage"] = can_manage
        if can_invite is not UNSET:
            field_dict["canInvite"] = can_invite
        if can_organize is not UNSET:
            field_dict["canOrganize"] = can_organize

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("userId")

        can_manage_household = d.pop("canManageHousehold", UNSET)

        can_manage = d.pop("canManage", UNSET)

        can_invite = d.pop("canInvite", UNSET)

        can_organize = d.pop("canOrganize", UNSET)

        set_permissions = cls(
            user_id=user_id,
            can_manage_household=can_manage_household,
            can_manage=can_manage,
            can_invite=can_invite,
            can_organize=can_organize,
        )

        set_permissions.additional_properties = d
        return set_permissions

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
