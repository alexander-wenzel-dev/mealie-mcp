from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ai_provider_create_requestheaders import AIProviderCreateRequestheaders
    from ..models.ai_provider_create_requestparams import AIProviderCreateRequestparams


T = TypeVar("T", bound="AIProviderCreate")


@_attrs_define
class AIProviderCreate:
    """
    Attributes:
        name (str):
        model (str):
        base_url (None | str | Unset):
        api_key (str | Unset):  Default: ''.
        timeout (int | Unset):  Default: 300.
        request_headers (AIProviderCreateRequestheaders | Unset):
        request_params (AIProviderCreateRequestparams | Unset):
    """

    name: str
    model: str
    base_url: None | str | Unset = UNSET
    api_key: str | Unset = ""
    timeout: int | Unset = 300
    request_headers: AIProviderCreateRequestheaders | Unset = UNSET
    request_params: AIProviderCreateRequestparams | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        model = self.model

        base_url: None | str | Unset
        if isinstance(self.base_url, Unset):
            base_url = UNSET
        else:
            base_url = self.base_url

        api_key = self.api_key

        timeout = self.timeout

        request_headers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.request_headers, Unset):
            request_headers = self.request_headers.to_dict()

        request_params: dict[str, Any] | Unset = UNSET
        if not isinstance(self.request_params, Unset):
            request_params = self.request_params.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "model": model,
            }
        )
        if base_url is not UNSET:
            field_dict["baseUrl"] = base_url
        if api_key is not UNSET:
            field_dict["apiKey"] = api_key
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if request_headers is not UNSET:
            field_dict["requestHeaders"] = request_headers
        if request_params is not UNSET:
            field_dict["requestParams"] = request_params

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ai_provider_create_requestheaders import AIProviderCreateRequestheaders
        from ..models.ai_provider_create_requestparams import AIProviderCreateRequestparams

        d = dict(src_dict)
        name = d.pop("name")

        model = d.pop("model")

        def _parse_base_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        base_url = _parse_base_url(d.pop("baseUrl", UNSET))

        api_key = d.pop("apiKey", UNSET)

        timeout = d.pop("timeout", UNSET)

        _request_headers = d.pop("requestHeaders", UNSET)
        request_headers: AIProviderCreateRequestheaders | Unset
        if isinstance(_request_headers, Unset):
            request_headers = UNSET
        else:
            request_headers = AIProviderCreateRequestheaders.from_dict(_request_headers)

        _request_params = d.pop("requestParams", UNSET)
        request_params: AIProviderCreateRequestparams | Unset
        if isinstance(_request_params, Unset):
            request_params = UNSET
        else:
            request_params = AIProviderCreateRequestparams.from_dict(_request_params)

        ai_provider_create = cls(
            name=name,
            model=model,
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            request_headers=request_headers,
            request_params=request_params,
        )

        ai_provider_create.additional_properties = d
        return ai_provider_create

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
