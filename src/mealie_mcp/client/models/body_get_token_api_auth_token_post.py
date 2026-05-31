from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyGetTokenApiAuthTokenPost")


@_attrs_define
class BodyGetTokenApiAuthTokenPost:
    """
    Attributes:
        username (str | Unset):  Default: ''.
        password (str | Unset):  Default: ''.
        remember_me (bool | Unset):  Default: False.
    """

    username: str | Unset = ""
    password: str | Unset = ""
    remember_me: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        password = self.password

        remember_me = self.remember_me

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password
        if remember_me is not UNSET:
            field_dict["remember_me"] = remember_me

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        remember_me = d.pop("remember_me", UNSET)

        body_get_token_api_auth_token_post = cls(
            username=username,
            password=password,
            remember_me=remember_me,
        )

        body_get_token_api_auth_token_post.additional_properties = d
        return body_get_token_api_auth_token_post

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
