from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ResetPassword")


@_attrs_define
class ResetPassword:
    """
    Attributes:
        token (str):
        email (str):
        password (str):
        password_confirm (str):
    """

    token: str
    email: str
    password: str
    password_confirm: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        email = self.email

        password = self.password

        password_confirm = self.password_confirm

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "email": email,
                "password": password,
                "passwordConfirm": password_confirm,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        email = d.pop("email")

        password = d.pop("password")

        password_confirm = d.pop("passwordConfirm")

        reset_password = cls(
            token=token,
            email=email,
            password=password,
            password_confirm=password_confirm,
        )

        reset_password.additional_properties = d
        return reset_password

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
