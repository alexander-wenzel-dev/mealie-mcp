from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AppInfo")


@_attrs_define
class AppInfo:
    """
    Attributes:
        production (bool):
        version (str):
        demo_status (bool):
        allow_signup (bool):
        allow_password_login (bool):
        enable_oidc (bool):
        oidc_redirect (bool):
        oidc_provider_name (str):
        token_time (int):
        default_group_slug (None | str | Unset):
        default_household_slug (None | str | Unset):
        allowed_iframe_hosts (list[str] | Unset):
    """

    production: bool
    version: str
    demo_status: bool
    allow_signup: bool
    allow_password_login: bool
    enable_oidc: bool
    oidc_redirect: bool
    oidc_provider_name: str
    token_time: int
    default_group_slug: None | str | Unset = UNSET
    default_household_slug: None | str | Unset = UNSET
    allowed_iframe_hosts: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        production = self.production

        version = self.version

        demo_status = self.demo_status

        allow_signup = self.allow_signup

        allow_password_login = self.allow_password_login

        enable_oidc = self.enable_oidc

        oidc_redirect = self.oidc_redirect

        oidc_provider_name = self.oidc_provider_name

        token_time = self.token_time

        default_group_slug: None | str | Unset
        if isinstance(self.default_group_slug, Unset):
            default_group_slug = UNSET
        else:
            default_group_slug = self.default_group_slug

        default_household_slug: None | str | Unset
        if isinstance(self.default_household_slug, Unset):
            default_household_slug = UNSET
        else:
            default_household_slug = self.default_household_slug

        allowed_iframe_hosts: list[str] | Unset = UNSET
        if not isinstance(self.allowed_iframe_hosts, Unset):
            allowed_iframe_hosts = self.allowed_iframe_hosts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "production": production,
                "version": version,
                "demoStatus": demo_status,
                "allowSignup": allow_signup,
                "allowPasswordLogin": allow_password_login,
                "enableOidc": enable_oidc,
                "oidcRedirect": oidc_redirect,
                "oidcProviderName": oidc_provider_name,
                "tokenTime": token_time,
            }
        )
        if default_group_slug is not UNSET:
            field_dict["defaultGroupSlug"] = default_group_slug
        if default_household_slug is not UNSET:
            field_dict["defaultHouseholdSlug"] = default_household_slug
        if allowed_iframe_hosts is not UNSET:
            field_dict["allowedIframeHosts"] = allowed_iframe_hosts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        production = d.pop("production")

        version = d.pop("version")

        demo_status = d.pop("demoStatus")

        allow_signup = d.pop("allowSignup")

        allow_password_login = d.pop("allowPasswordLogin")

        enable_oidc = d.pop("enableOidc")

        oidc_redirect = d.pop("oidcRedirect")

        oidc_provider_name = d.pop("oidcProviderName")

        token_time = d.pop("tokenTime")

        def _parse_default_group_slug(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_group_slug = _parse_default_group_slug(d.pop("defaultGroupSlug", UNSET))

        def _parse_default_household_slug(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_household_slug = _parse_default_household_slug(d.pop("defaultHouseholdSlug", UNSET))

        allowed_iframe_hosts = cast(list[str], d.pop("allowedIframeHosts", UNSET))

        app_info = cls(
            production=production,
            version=version,
            demo_status=demo_status,
            allow_signup=allow_signup,
            allow_password_login=allow_password_login,
            enable_oidc=enable_oidc,
            oidc_redirect=oidc_redirect,
            oidc_provider_name=oidc_provider_name,
            token_time=token_time,
            default_group_slug=default_group_slug,
            default_household_slug=default_household_slug,
            allowed_iframe_hosts=allowed_iframe_hosts,
        )

        app_info.additional_properties = d
        return app_info

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
