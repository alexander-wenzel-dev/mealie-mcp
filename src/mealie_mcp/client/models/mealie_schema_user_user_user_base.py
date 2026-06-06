from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_method import AuthMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="MealieSchemaUserUserUserBase")


@_attrs_define
class MealieSchemaUserUserUserBase:
    """
    Example:
        {'admin': 'false', 'email': 'changeme@example.com', 'fullName': 'Change Me', 'group': 'Home', 'household':
            'Family', 'username': 'ChangeMe'}

    Attributes:
        email (str):
        id (None | str | Unset):
        username (None | str | Unset):
        full_name (None | str | Unset):
        auth_method (AuthMethod | Unset):
        admin (bool | Unset):  Default: False.
        group (None | str | Unset):
        household (None | str | Unset):
        advanced (bool | Unset):  Default: False.
        show_announcements (bool | Unset):  Default: True.
        last_read_announcement (None | str | Unset):
        can_invite (bool | Unset):  Default: False.
        can_manage (bool | Unset):  Default: False.
        can_manage_household (bool | Unset):  Default: False.
        can_organize (bool | Unset):  Default: False.
    """

    email: str
    id: None | str | Unset = UNSET
    username: None | str | Unset = UNSET
    full_name: None | str | Unset = UNSET
    auth_method: AuthMethod | Unset = UNSET
    admin: bool | Unset = False
    group: None | str | Unset = UNSET
    household: None | str | Unset = UNSET
    advanced: bool | Unset = False
    show_announcements: bool | Unset = True
    last_read_announcement: None | str | Unset = UNSET
    can_invite: bool | Unset = False
    can_manage: bool | Unset = False
    can_manage_household: bool | Unset = False
    can_organize: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        username: None | str | Unset
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        full_name: None | str | Unset
        if isinstance(self.full_name, Unset):
            full_name = UNSET
        else:
            full_name = self.full_name

        auth_method: str | Unset = UNSET
        if not isinstance(self.auth_method, Unset):
            auth_method = self.auth_method.value

        admin = self.admin

        group: None | str | Unset
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group

        household: None | str | Unset
        if isinstance(self.household, Unset):
            household = UNSET
        else:
            household = self.household

        advanced = self.advanced

        show_announcements = self.show_announcements

        last_read_announcement: None | str | Unset
        if isinstance(self.last_read_announcement, Unset):
            last_read_announcement = UNSET
        else:
            last_read_announcement = self.last_read_announcement

        can_invite = self.can_invite

        can_manage = self.can_manage

        can_manage_household = self.can_manage_household

        can_organize = self.can_organize

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if username is not UNSET:
            field_dict["username"] = username
        if full_name is not UNSET:
            field_dict["fullName"] = full_name
        if auth_method is not UNSET:
            field_dict["authMethod"] = auth_method
        if admin is not UNSET:
            field_dict["admin"] = admin
        if group is not UNSET:
            field_dict["group"] = group
        if household is not UNSET:
            field_dict["household"] = household
        if advanced is not UNSET:
            field_dict["advanced"] = advanced
        if show_announcements is not UNSET:
            field_dict["showAnnouncements"] = show_announcements
        if last_read_announcement is not UNSET:
            field_dict["lastReadAnnouncement"] = last_read_announcement
        if can_invite is not UNSET:
            field_dict["canInvite"] = can_invite
        if can_manage is not UNSET:
            field_dict["canManage"] = can_manage
        if can_manage_household is not UNSET:
            field_dict["canManageHousehold"] = can_manage_household
        if can_organize is not UNSET:
            field_dict["canOrganize"] = can_organize

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_username(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        username = _parse_username(d.pop("username", UNSET))

        def _parse_full_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        full_name = _parse_full_name(d.pop("fullName", UNSET))

        _auth_method = d.pop("authMethod", UNSET)
        auth_method: AuthMethod | Unset
        if isinstance(_auth_method, Unset):
            auth_method = UNSET
        else:
            auth_method = AuthMethod(_auth_method)

        admin = d.pop("admin", UNSET)

        def _parse_group(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group = _parse_group(d.pop("group", UNSET))

        def _parse_household(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        household = _parse_household(d.pop("household", UNSET))

        advanced = d.pop("advanced", UNSET)

        show_announcements = d.pop("showAnnouncements", UNSET)

        def _parse_last_read_announcement(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_read_announcement = _parse_last_read_announcement(d.pop("lastReadAnnouncement", UNSET))

        can_invite = d.pop("canInvite", UNSET)

        can_manage = d.pop("canManage", UNSET)

        can_manage_household = d.pop("canManageHousehold", UNSET)

        can_organize = d.pop("canOrganize", UNSET)

        mealie_schema_user_user_user_base = cls(
            email=email,
            id=id,
            username=username,
            full_name=full_name,
            auth_method=auth_method,
            admin=admin,
            group=group,
            household=household,
            advanced=advanced,
            show_announcements=show_announcements,
            last_read_announcement=last_read_announcement,
            can_invite=can_invite,
            can_manage=can_manage,
            can_manage_household=can_manage_household,
            can_organize=can_organize,
        )

        mealie_schema_user_user_user_base.additional_properties = d
        return mealie_schema_user_user_user_base

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
