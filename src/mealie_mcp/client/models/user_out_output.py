from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_method import AuthMethod

if TYPE_CHECKING:
    from ..models.long_live_token_out_output import LongLiveTokenOutOutput


T = TypeVar("T", bound="UserOutOutput")


@_attrs_define
class UserOutOutput:
    """
    Example:
        {'admin': 'false', 'email': 'changeme@example.com', 'fullName': 'Change Me', 'group': 'Home', 'household':
            'Family', 'username': 'ChangeMe'}

    Attributes:
        id (str):
        username (None | str):
        full_name (None | str):
        email (str):
        auth_method (AuthMethod):
        admin (bool):  Default: False.
        group (str):
        household (str):
        advanced (bool):  Default: False.
        show_announcements (bool):  Default: True.
        last_read_announcement (None | str):
        can_invite (bool):  Default: False.
        can_manage (bool):  Default: False.
        can_manage_household (bool):  Default: False.
        can_organize (bool):  Default: False.
        group_id (str):
        group_slug (str):
        household_id (str):
        household_slug (str):
        tokens (list[LongLiveTokenOutOutput] | None):
        cache_key (str):
    """

    id: str
    username: str | None
    full_name: str | None
    email: str
    auth_method: AuthMethod
    group: str
    household: str
    last_read_announcement: str | None
    group_id: str
    group_slug: str
    household_id: str
    household_slug: str
    tokens: list[LongLiveTokenOutOutput] | None
    cache_key: str
    admin: bool = False
    advanced: bool = False
    show_announcements: bool = True
    can_invite: bool = False
    can_manage: bool = False
    can_manage_household: bool = False
    can_organize: bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        username: str | None
        username = self.username

        full_name: str | None
        full_name = self.full_name

        email = self.email

        auth_method = self.auth_method.value

        admin = self.admin

        group = self.group

        household = self.household

        advanced = self.advanced

        show_announcements = self.show_announcements

        last_read_announcement: str | None
        last_read_announcement = self.last_read_announcement

        can_invite = self.can_invite

        can_manage = self.can_manage

        can_manage_household = self.can_manage_household

        can_organize = self.can_organize

        group_id = self.group_id

        group_slug = self.group_slug

        household_id = self.household_id

        household_slug = self.household_slug

        tokens: list[dict[str, Any]] | None
        if isinstance(self.tokens, list):
            tokens = []
            for tokens_type_0_item_data in self.tokens:
                tokens_type_0_item = tokens_type_0_item_data.to_dict()
                tokens.append(tokens_type_0_item)

        else:
            tokens = self.tokens

        cache_key = self.cache_key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "username": username,
                "fullName": full_name,
                "email": email,
                "authMethod": auth_method,
                "admin": admin,
                "group": group,
                "household": household,
                "advanced": advanced,
                "showAnnouncements": show_announcements,
                "lastReadAnnouncement": last_read_announcement,
                "canInvite": can_invite,
                "canManage": can_manage,
                "canManageHousehold": can_manage_household,
                "canOrganize": can_organize,
                "groupId": group_id,
                "groupSlug": group_slug,
                "householdId": household_id,
                "householdSlug": household_slug,
                "tokens": tokens,
                "cacheKey": cache_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.long_live_token_out_output import LongLiveTokenOutOutput  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_username(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        username = _parse_username(d.pop("username"))

        def _parse_full_name(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        full_name = _parse_full_name(d.pop("fullName"))

        email = d.pop("email")

        auth_method = AuthMethod(d.pop("authMethod"))

        admin = d.pop("admin")

        group = d.pop("group")

        household = d.pop("household")

        advanced = d.pop("advanced")

        show_announcements = d.pop("showAnnouncements")

        def _parse_last_read_announcement(data: object) -> str | None:
            if data is None:
                return data
            return cast(None | str, data)

        last_read_announcement = _parse_last_read_announcement(d.pop("lastReadAnnouncement"))

        can_invite = d.pop("canInvite")

        can_manage = d.pop("canManage")

        can_manage_household = d.pop("canManageHousehold")

        can_organize = d.pop("canOrganize")

        group_id = d.pop("groupId")

        group_slug = d.pop("groupSlug")

        household_id = d.pop("householdId")

        household_slug = d.pop("householdSlug")

        def _parse_tokens(data: object) -> list[LongLiveTokenOutOutput] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tokens_type_0 = []
                _tokens_type_0 = data
                for tokens_type_0_item_data in _tokens_type_0:
                    tokens_type_0_item = LongLiveTokenOutOutput.from_dict(tokens_type_0_item_data)

                    tokens_type_0.append(tokens_type_0_item)

                return tokens_type_0
            except TypeError, ValueError, AttributeError, KeyError:
                pass
            return cast(list[LongLiveTokenOutOutput] | None, data)

        tokens = _parse_tokens(d.pop("tokens"))

        cache_key = d.pop("cacheKey")

        user_out_output = cls(
            id=id,
            username=username,
            full_name=full_name,
            email=email,
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
            group_id=group_id,
            group_slug=group_slug,
            household_id=household_id,
            household_slug=household_slug,
            tokens=tokens,
            cache_key=cache_key,
        )

        user_out_output.additional_properties = d
        return user_out_output

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
