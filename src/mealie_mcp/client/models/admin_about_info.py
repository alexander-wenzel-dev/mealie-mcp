from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminAboutInfo")


@_attrs_define
class AdminAboutInfo:
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
        version_latest (str):
        api_port (int):
        api_docs (bool):
        db_type (str):
        default_group (str):
        default_household (str):
        build_id (str):
        recipe_scraper_version (str):
        default_group_slug (None | str | Unset):
        default_household_slug (None | str | Unset):
        allowed_iframe_hosts (list[str] | Unset):
        db_url (None | str | Unset):
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
    version_latest: str
    api_port: int
    api_docs: bool
    db_type: str
    default_group: str
    default_household: str
    build_id: str
    recipe_scraper_version: str
    default_group_slug: None | str | Unset = UNSET
    default_household_slug: None | str | Unset = UNSET
    allowed_iframe_hosts: list[str] | Unset = UNSET
    db_url: None | str | Unset = UNSET
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

        version_latest = self.version_latest

        api_port = self.api_port

        api_docs = self.api_docs

        db_type = self.db_type

        default_group = self.default_group

        default_household = self.default_household

        build_id = self.build_id

        recipe_scraper_version = self.recipe_scraper_version

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

        db_url: None | str | Unset
        if isinstance(self.db_url, Unset):
            db_url = UNSET
        else:
            db_url = self.db_url

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
                "versionLatest": version_latest,
                "apiPort": api_port,
                "apiDocs": api_docs,
                "dbType": db_type,
                "defaultGroup": default_group,
                "defaultHousehold": default_household,
                "buildId": build_id,
                "recipeScraperVersion": recipe_scraper_version,
            }
        )
        if default_group_slug is not UNSET:
            field_dict["defaultGroupSlug"] = default_group_slug
        if default_household_slug is not UNSET:
            field_dict["defaultHouseholdSlug"] = default_household_slug
        if allowed_iframe_hosts is not UNSET:
            field_dict["allowedIframeHosts"] = allowed_iframe_hosts
        if db_url is not UNSET:
            field_dict["dbUrl"] = db_url

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

        version_latest = d.pop("versionLatest")

        api_port = d.pop("apiPort")

        api_docs = d.pop("apiDocs")

        db_type = d.pop("dbType")

        default_group = d.pop("defaultGroup")

        default_household = d.pop("defaultHousehold")

        build_id = d.pop("buildId")

        recipe_scraper_version = d.pop("recipeScraperVersion")

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

        def _parse_db_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        db_url = _parse_db_url(d.pop("dbUrl", UNSET))

        admin_about_info = cls(
            production=production,
            version=version,
            demo_status=demo_status,
            allow_signup=allow_signup,
            allow_password_login=allow_password_login,
            enable_oidc=enable_oidc,
            oidc_redirect=oidc_redirect,
            oidc_provider_name=oidc_provider_name,
            token_time=token_time,
            version_latest=version_latest,
            api_port=api_port,
            api_docs=api_docs,
            db_type=db_type,
            default_group=default_group,
            default_household=default_household,
            build_id=build_id,
            recipe_scraper_version=recipe_scraper_version,
            default_group_slug=default_group_slug,
            default_household_slug=default_household_slug,
            allowed_iframe_hosts=allowed_iframe_hosts,
            db_url=db_url,
        )

        admin_about_info.additional_properties = d
        return admin_about_info

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
