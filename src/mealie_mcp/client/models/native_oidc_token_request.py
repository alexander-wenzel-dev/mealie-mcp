from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NativeOIDCTokenRequest")


@_attrs_define
class NativeOIDCTokenRequest:
    """An authorization code captured by a native client, for server-side exchange.

    Attributes:
        code (str):
        code_verifier (str):
        redirect_uri (str):
        nonce (None | str | Unset):
    """

    code: str
    code_verifier: str
    redirect_uri: str
    nonce: str | Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        code_verifier = self.code_verifier

        redirect_uri = self.redirect_uri

        nonce: str | Unset | None
        if isinstance(self.nonce, Unset):
            nonce = UNSET
        else:
            nonce = self.nonce

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "code_verifier": code_verifier,
                "redirect_uri": redirect_uri,
            }
        )
        if nonce is not UNSET:
            field_dict["nonce"] = nonce

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = d.pop("code")

        code_verifier = d.pop("code_verifier")

        redirect_uri = d.pop("redirect_uri")

        def _parse_nonce(data: object) -> str | Unset | None:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        nonce = _parse_nonce(d.pop("nonce", UNSET))

        native_oidc_token_request = cls(
            code=code,
            code_verifier=code_verifier,
            redirect_uri=redirect_uri,
            nonce=nonce,
        )

        native_oidc_token_request.additional_properties = d
        return native_oidc_token_request

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
