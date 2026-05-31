from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_method import AuthMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.long_live_token_out import LongLiveTokenOut


T = TypeVar("T", bound="UserOut")


@_attrs_define
class UserOut:
    """
    Example:
        {'admin': 'false', 'email': 'changeme@example.com', 'fullName': 'Change Me', 'group': 'Home', 'household':
            'Family', 'username': 'ChangeMe'}

    Attributes:
        id (str):
        email (str):
        group (str):
        household (str):
        group_id (str):
        group_slug (str):
        household_id (str):
        household_slug (str):
        cache_key (str):
        username (None | str | Unset):
        full_name (None | str | Unset):
        auth_method (AuthMethod | Unset):
        admin (bool | Unset):  Default: False.
        advanced (bool | Unset):  Default: False.
        show_announcements (bool | Unset):  Default: True.
        last_read_announcement (None | str | Unset):
        can_invite (bool | Unset):  Default: False.
        can_manage (bool | Unset):  Default: False.
        can_manage_household (bool | Unset):  Default: False.
        can_organize (bool | Unset):  Default: False.
        tokens (list[LongLiveTokenOut] | None | Unset):
    """

    id: str
    email: str
    group: str
    household: str
    group_id: str
    group_slug: str
    household_id: str
    household_slug: str
    cache_key: str
    username: None | str | Unset = UNSET
    full_name: None | str | Unset = UNSET
    auth_method: AuthMethod | Unset = UNSET
    admin: bool | Unset = False
    advanced: bool | Unset = False
    show_announcements: bool | Unset = True
    last_read_announcement: None | str | Unset = UNSET
    can_invite: bool | Unset = False
    can_manage: bool | Unset = False
    can_manage_household: bool | Unset = False
    can_organize: bool | Unset = False
    tokens: list[LongLiveTokenOut] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        email = self.email

        group = self.group

        household = self.household

        group_id = self.group_id

        group_slug = self.group_slug

        household_id = self.household_id

        household_slug = self.household_slug

        cache_key = self.cache_key

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

        tokens: list[dict[str, Any]] | None | Unset
        if isinstance(self.tokens, Unset):
            tokens = UNSET
        elif isinstance(self.tokens, list):
            tokens = []
            for tokens_type_0_item_data in self.tokens:
                tokens_type_0_item = tokens_type_0_item_data.to_dict()
                tokens.append(tokens_type_0_item)

        else:
            tokens = self.tokens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "email": email,
                "group": group,
                "household": household,
                "groupId": group_id,
                "groupSlug": group_slug,
                "householdId": household_id,
                "householdSlug": household_slug,
                "cacheKey": cache_key,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if full_name is not UNSET:
            field_dict["fullName"] = full_name
        if auth_method is not UNSET:
            field_dict["authMethod"] = auth_method
        if admin is not UNSET:
            field_dict["admin"] = admin
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
        if tokens is not UNSET:
            field_dict["tokens"] = tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.long_live_token_out import LongLiveTokenOut

        d = dict(src_dict)
        id = d.pop("id")

        email = d.pop("email")

        group = d.pop("group")

        household = d.pop("household")

        group_id = d.pop("groupId")

        group_slug = d.pop("groupSlug")

        household_id = d.pop("householdId")

        household_slug = d.pop("householdSlug")

        cache_key = d.pop("cacheKey")

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

        def _parse_tokens(data: object) -> list[LongLiveTokenOut] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tokens_type_0 = []
                _tokens_type_0 = data
                for tokens_type_0_item_data in _tokens_type_0:
                    tokens_type_0_item = LongLiveTokenOut.from_dict(tokens_type_0_item_data)

                    tokens_type_0.append(tokens_type_0_item)

                return tokens_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[LongLiveTokenOut] | None | Unset, data)

        tokens = _parse_tokens(d.pop("tokens", UNSET))

        user_out = cls(
            id=id,
            email=email,
            group=group,
            household=household,
            group_id=group_id,
            group_slug=group_slug,
            household_id=household_id,
            household_slug=household_slug,
            cache_key=cache_key,
            username=username,
            full_name=full_name,
            auth_method=auth_method,
            admin=admin,
            advanced=advanced,
            show_announcements=show_announcements,
            last_read_announcement=last_read_announcement,
            can_invite=can_invite,
            can_manage=can_manage,
            can_manage_household=can_manage_household,
            can_organize=can_organize,
            tokens=tokens,
        )

        user_out.additional_properties = d
        return user_out

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
