from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUserRegistration")


@_attrs_define
class CreateUserRegistration:
    """
    Attributes:
        email (str):
        username (str):
        full_name (str):
        password (str):
        password_confirm (str):
        group (None | str | Unset):
        household (None | str | Unset):
        group_token (None | str | Unset):
        advanced (bool | Unset):  Default: False.
        private (bool | Unset):  Default: False.
        seed_data (bool | Unset):  Default: False.
        locale (str | Unset):  Default: 'en-US'.
    """

    email: str
    username: str
    full_name: str
    password: str
    password_confirm: str
    group: None | str | Unset = UNSET
    household: None | str | Unset = UNSET
    group_token: None | str | Unset = UNSET
    advanced: bool | Unset = False
    private: bool | Unset = False
    seed_data: bool | Unset = False
    locale: str | Unset = "en-US"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        username = self.username

        full_name = self.full_name

        password = self.password

        password_confirm = self.password_confirm

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

        group_token: None | str | Unset
        if isinstance(self.group_token, Unset):
            group_token = UNSET
        else:
            group_token = self.group_token

        advanced = self.advanced

        private = self.private

        seed_data = self.seed_data

        locale = self.locale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "username": username,
                "fullName": full_name,
                "password": password,
                "passwordConfirm": password_confirm,
            }
        )
        if group is not UNSET:
            field_dict["group"] = group
        if household is not UNSET:
            field_dict["household"] = household
        if group_token is not UNSET:
            field_dict["groupToken"] = group_token
        if advanced is not UNSET:
            field_dict["advanced"] = advanced
        if private is not UNSET:
            field_dict["private"] = private
        if seed_data is not UNSET:
            field_dict["seedData"] = seed_data
        if locale is not UNSET:
            field_dict["locale"] = locale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        username = d.pop("username")

        full_name = d.pop("fullName")

        password = d.pop("password")

        password_confirm = d.pop("passwordConfirm")

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

        def _parse_group_token(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_token = _parse_group_token(d.pop("groupToken", UNSET))

        advanced = d.pop("advanced", UNSET)

        private = d.pop("private", UNSET)

        seed_data = d.pop("seedData", UNSET)

        locale = d.pop("locale", UNSET)

        create_user_registration = cls(
            email=email,
            username=username,
            full_name=full_name,
            password=password,
            password_confirm=password_confirm,
            group=group,
            household=household,
            group_token=group_token,
            advanced=advanced,
            private=private,
            seed_data=seed_data,
            locale=locale,
        )

        create_user_registration.additional_properties = d
        return create_user_registration

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
