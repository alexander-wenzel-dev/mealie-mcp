from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CheckAppConfig")


@_attrs_define
class CheckAppConfig:
    """
    Attributes:
        email_ready (bool):
        ldap_ready (bool):
        oidc_ready (bool):
        base_url_set (bool):
        is_up_to_date (bool):
    """

    email_ready: bool
    ldap_ready: bool
    oidc_ready: bool
    base_url_set: bool
    is_up_to_date: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email_ready = self.email_ready

        ldap_ready = self.ldap_ready

        oidc_ready = self.oidc_ready

        base_url_set = self.base_url_set

        is_up_to_date = self.is_up_to_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "emailReady": email_ready,
                "ldapReady": ldap_ready,
                "oidcReady": oidc_ready,
                "baseUrlSet": base_url_set,
                "isUpToDate": is_up_to_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email_ready = d.pop("emailReady")

        ldap_ready = d.pop("ldapReady")

        oidc_ready = d.pop("oidcReady")

        base_url_set = d.pop("baseUrlSet")

        is_up_to_date = d.pop("isUpToDate")

        check_app_config = cls(
            email_ready=email_ready,
            ldap_ready=ldap_ready,
            oidc_ready=oidc_ready,
            base_url_set=base_url_set,
            is_up_to_date=is_up_to_date,
        )

        check_app_config.additional_properties = d
        return check_app_config

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
